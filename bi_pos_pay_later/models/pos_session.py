# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, tools
from odoo.exceptions import RedirectWarning, UserError, ValidationError, Warning
import random
import base64
from datetime import date, datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from collections import defaultdict
from odoo.tools import float_is_zero


class PosSessionInherit(models.Model):
	_inherit = 'pos.session'

	@api.model
	def create(self, vals):
		res = super(PosSessionInherit, self).create(vals)
		orders = self.env['pos.order'].search([('user_id', '=', self.env.uid),
											   ('state', '=', 'draft'), ('session_id.state', '=', 'closed')])
		orders.write({'session_id': res.id})
		return res

	def action_pos_session_closing_control(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
		bank_payment_method_diffs = bank_payment_method_diffs or {}
		self._check_pos_session_balance()
		for session in self:
			orders = session.order_ids.filtered(lambda order: order.is_partial == False)
			if any(order.state == 'draft' for order in orders):
				raise UserError(_("You cannot close the POS when orders are still in draft"))
			if session.state == 'closed':
				raise UserError(_('This session is already closed.'))
			session.write({'state': 'closing_control', 'stop_at': fields.Datetime.now()})
			if not session.config_id.cash_control:
				return session.action_pos_session_close(balancing_account, amount_to_balance, bank_payment_method_diffs)
			# If the session is in rescue, we only compute the payments in the cash register
			# It is not yet possible to close a rescue session through the front end, see `close_session_from_ui`
			if session.rescue and session.config_id.cash_control:
				default_cash_payment_method_id = self.payment_method_ids.filtered(lambda pm: pm.type == 'cash')[0]
				orders = self.order_ids.filtered(lambda o: o.state == 'paid' or o.state == 'invoiced')
				total_cash = sum(
					orders.payment_ids.filtered(lambda p: p.payment_method_id == default_cash_payment_method_id).mapped('amount')
				) + self.cash_register_balance_start

				session.cash_register_id.balance_end_real = total_cash

			return session.action_pos_session_validate(balancing_account, amount_to_balance, bank_payment_method_diffs)

	def _check_if_no_draft_orders(self):
		draft_orders = self.order_ids.filtered(lambda order: order.state == 'draft')
		do = []
		for i in draft_orders:
			if not i.is_partial:
				do.append(i.name)
		if do:
			raise UserError(_(
				'There are still orders in draft state in the session. '
				'Pay or cancel the following orders to validate the session:\n%s'
			) % ', '.join(do)
							)
		return True

	def _cannot_close_session(self, bank_payment_method_diffs=None):
		"""
		Add check in this method if you want to return or raise an error when trying to either post cash details
		or close the session. Raising an error will always redirect the user to the back end.
		It should return {'successful': False, 'message': str, 'redirect': bool} if we can't close the session
		"""
		bank_payment_method_diffs = bank_payment_method_diffs or {}
		orders = self.order_ids.filtered(lambda order: order.is_partial == False)
		if any(order.state == 'draft' for order in orders):
			return {'successful': False, 'message': _("You cannot close the POS when orders are still in draft"), 'redirect': False}
		if self.state == 'closed':
			return {'successful': False, 'message': _("This session is already closed."), 'redirect': True}
		if bank_payment_method_diffs:
			no_loss_account = self.env['account.journal']
			no_profit_account = self.env['account.journal']
			for payment_method in self.env['pos.payment.method'].browse(bank_payment_method_diffs.keys()):
				journal = payment_method.journal_id
				compare_to_zero = self.currency_id.compare_amounts(bank_payment_method_diffs.get(payment_method.id), 0)
				if compare_to_zero == -1 and not journal.loss_account_id:
					no_loss_account |= journal
				elif compare_to_zero == 1 and not journal.profit_account_id:
					no_profit_account |= journal
			message = ''
			if no_loss_account:
				message += _("Need loss account for the following journals to post the lost amount: %s\n", ', '.join(no_loss_account.mapped('name')))
			if no_profit_account:
				message += _("Need profit account for the following journals to post the gained amount: %s", ', '.join(no_profit_account.mapped('name')))
			if message:
				return {'successful': False, 'message': message, 'redirect': False}



	def _accumulate_amounts(self, data):
		# Accumulate the amounts for each accounting lines group
		# Each dict maps `key` -> `amounts`, where `key` is the group key.
		# E.g. `combine_receivables_bank` is derived from pos.payment records
		# in the self.order_ids with group key of the `payment_method_id`
		# field of the pos.payment record.
		amounts = lambda: {'amount': 0.0, 'amount_converted': 0.0}
		tax_amounts = lambda: {'amount': 0.0, 'amount_converted': 0.0, 'base_amount': 0.0, 'base_amount_converted': 0.0}
		split_receivables_bank = defaultdict(amounts)
		split_receivables_cash = defaultdict(amounts)
		split_receivables_pay_later = defaultdict(amounts)
		combine_receivables_bank = defaultdict(amounts)
		combine_receivables_cash = defaultdict(amounts)
		combine_receivables_pay_later = defaultdict(amounts)
		combine_invoice_receivables = defaultdict(amounts)
		split_invoice_receivables = defaultdict(amounts)
		sales = defaultdict(amounts)
		taxes = defaultdict(tax_amounts)
		stock_expense = defaultdict(amounts)
		stock_return = defaultdict(amounts)
		stock_output = defaultdict(amounts)
		rounding_difference = {'amount': 0.0, 'amount_converted': 0.0}
		# Track the receivable lines of the order's invoice payment moves for reconciliation
		# These receivable lines are reconciled to the corresponding invoice receivable lines
		# of this session's move_id.
		combine_inv_payment_receivable_lines = defaultdict(lambda: self.env['account.move.line'])
		split_inv_payment_receivable_lines = defaultdict(lambda: self.env['account.move.line'])
		rounded_globally = self.company_id.tax_calculation_rounding_method == 'round_globally'
		pos_receivable_account = self.company_id.account_default_pos_receivable_account_id
		currency_rounding = self.currency_id.rounding
		order_ids = self.order_ids.filtered(lambda order: order.is_partial == False)
		for order in order_ids:
			order_is_invoiced = order.is_invoiced
			for payment in order.payment_ids:
				amount = payment.amount
				if float_is_zero(amount, precision_rounding=currency_rounding):
					continue
				date = payment.payment_date
				payment_method = payment.payment_method_id
				is_split_payment = payment.payment_method_id.split_transactions
				payment_type = payment_method.type

				# If not pay_later, we create the receivable vals for both invoiced and uninvoiced orders.
				#   Separate the split and aggregated payments.
				# Moreover, if the order is invoiced, we create the pos receivable vals that will balance the
				# pos receivable lines from the invoice payments.
				if payment_type != 'pay_later':
					if is_split_payment and payment_type == 'cash':
						split_receivables_cash[payment] = self._update_amounts(split_receivables_cash[payment], {'amount': amount}, date)
					elif not is_split_payment and payment_type == 'cash':
						combine_receivables_cash[payment_method] = self._update_amounts(combine_receivables_cash[payment_method], {'amount': amount}, date)
					elif is_split_payment and payment_type == 'bank':
						split_receivables_bank[payment] = self._update_amounts(split_receivables_bank[payment], {'amount': amount}, date)
					elif not is_split_payment and payment_type == 'bank':
						combine_receivables_bank[payment_method] = self._update_amounts(combine_receivables_bank[payment_method], {'amount': amount}, date)

					# Create the vals to create the pos receivables that will balance the pos receivables from invoice payment moves.
					if order_is_invoiced:
						if is_split_payment:
							split_inv_payment_receivable_lines[payment] |= payment.account_move_id.line_ids.filtered(lambda line: line.account_id == pos_receivable_account)
							split_invoice_receivables[payment] = self._update_amounts(split_invoice_receivables[payment], {'amount': payment.amount}, order.date_order)
						else:
							combine_inv_payment_receivable_lines[payment_method] |= payment.account_move_id.line_ids.filtered(lambda line: line.account_id == pos_receivable_account)
							combine_invoice_receivables[payment_method] = self._update_amounts(combine_invoice_receivables[payment_method], {'amount': payment.amount}, order.date_order)

				# If pay_later, we create the receivable lines.
				#   if split, with partner
				#   Otherwise, it's aggregated (combined)
				# But only do if order is *not* invoiced because no account move is created for pay later invoice payments.
				if payment_type == 'pay_later' and not order_is_invoiced:
					if is_split_payment:
						split_receivables_pay_later[payment] = self._update_amounts(split_receivables_pay_later[payment], {'amount': amount}, date)
					elif not is_split_payment:
						combine_receivables_pay_later[payment_method] = self._update_amounts(combine_receivables_pay_later[payment_method], {'amount': amount}, date)

			if not order_is_invoiced:
				order_taxes = defaultdict(tax_amounts)
				for order_line in order.lines:
					line = self._prepare_line(order_line)
					# Combine sales/refund lines
					sale_key = (
						# account
						line['income_account_id'],
						# sign
						-1 if line['amount'] < 0 else 1,
						# for taxes
						tuple((tax['id'], tax['account_id'], tax['tax_repartition_line_id']) for tax in line['taxes']),
						line['base_tags'],
					)
					sales[sale_key] = self._update_amounts(sales[sale_key], {'amount': line['amount']}, line['date_order'])
					# Combine tax lines
					for tax in line['taxes']:
						tax_key = (tax['account_id'], tax['tax_repartition_line_id'], tax['id'], tuple(tax['tag_ids']))
						order_taxes[tax_key] = self._update_amounts(
							order_taxes[tax_key],
							{'amount': tax['amount'], 'base_amount': tax['base']},
							tax['date_order'],
							round=not rounded_globally
						)
				for tax_key, amounts in order_taxes.items():
					if rounded_globally:
						amounts = self._round_amounts(amounts)
					for amount_key, amount in amounts.items():
						taxes[tax_key][amount_key] += amount

				if self.company_id.anglo_saxon_accounting and order.picking_ids.ids:
					# Combine stock lines
					stock_moves = self.env['stock.move'].sudo().search([
						('picking_id', 'in', order.picking_ids.ids),
						('company_id.anglo_saxon_accounting', '=', True),
						('product_id.categ_id.property_valuation', '=', 'real_time')
					])
					for move in stock_moves:
						exp_key = move.product_id._get_product_accounts()['expense']
						out_key = move.product_id.categ_id.property_stock_account_output_categ_id
						amount = -sum(move.sudo().stock_valuation_layer_ids.mapped('value'))
						stock_expense[exp_key] = self._update_amounts(stock_expense[exp_key], {'amount': amount}, move.picking_id.date, force_company_currency=True)
						if move.location_id.usage == 'customer':
							stock_return[out_key] = self._update_amounts(stock_return[out_key], {'amount': amount}, move.picking_id.date, force_company_currency=True)
						else:
							stock_output[out_key] = self._update_amounts(stock_output[out_key], {'amount': amount}, move.picking_id.date, force_company_currency=True)

				if self.config_id.cash_rounding:
					diff = order.amount_paid - order.amount_total
					rounding_difference = self._update_amounts(rounding_difference, {'amount': diff}, order.date_order)

				# Increasing current partner's customer_rank
				partners = (order.partner_id | order.partner_id.commercial_partner_id)
				partners._increase_rank('customer_rank')

		if self.company_id.anglo_saxon_accounting:
			global_session_pickings = self.picking_ids.filtered(lambda p: not p.pos_order_id)
			if global_session_pickings:
				stock_moves = self.env['stock.move'].sudo().search([
					('picking_id', 'in', global_session_pickings.ids),
					('company_id.anglo_saxon_accounting', '=', True),
					('product_id.categ_id.property_valuation', '=', 'real_time'),
				])
				for move in stock_moves:
					exp_key = move.product_id._get_product_accounts()['expense']
					out_key = move.product_id.categ_id.property_stock_account_output_categ_id
					amount = -sum(move.stock_valuation_layer_ids.mapped('value'))
					stock_expense[exp_key] = self._update_amounts(stock_expense[exp_key], {'amount': amount}, move.picking_id.date, force_company_currency=True)
					if move.location_id.usage == 'customer':
						stock_return[out_key] = self._update_amounts(stock_return[out_key], {'amount': amount}, move.picking_id.date, force_company_currency=True)
					else:
						stock_output[out_key] = self._update_amounts(stock_output[out_key], {'amount': amount}, move.picking_id.date, force_company_currency=True)
		MoveLine = self.env['account.move.line'].with_context(check_move_validity=False)

		data.update({
			'taxes':                               taxes,
			'sales':                               sales,
			'stock_expense':                       stock_expense,
			'split_receivables_bank':              split_receivables_bank,
			'combine_receivables_bank':            combine_receivables_bank,
			'split_receivables_cash':              split_receivables_cash,
			'combine_receivables_cash':            combine_receivables_cash,
			'combine_invoice_receivables':         combine_invoice_receivables,
			'split_receivables_pay_later':         split_receivables_pay_later,
			'combine_receivables_pay_later':       combine_receivables_pay_later,
			'stock_return':                        stock_return,
			'stock_output':                        stock_output,
			'combine_inv_payment_receivable_lines': combine_inv_payment_receivable_lines,
			'rounding_difference':                 rounding_difference,
			'MoveLine':                            MoveLine,
			'split_invoice_receivables': split_invoice_receivables,
			'split_inv_payment_receivable_lines': split_inv_payment_receivable_lines,
		})
		return data

