"""
    def create_move_values(self):
        for request in self:
            ref = request.name
            account_date = fields.Date.today()#self.date
            journal = request.journal
            company = request.company_id
            analytic_account = request.analytic_account
            move_value = {
                'ref':ref,
                'date': account_date,
                'journal_id': journal.id,
                'company_id': company.id,
            }
            expense_line_ids = []
            lines = request.mapped('line_ids')
            for line in lines:
                if not (line.employee_id.address_home_id.property_account_receivable_id):
                    raise UserError(_('Pas de compte pour : "%s" !') % (line.employee_id))
                partner_id = line.employee_id.address_home_id.id
                debit_account = line.employee_id.address_home_id.property_account_receivable_id if line.payment_mode == 'justify' else line.debit_account
                debit_line = (0, 0, {#received
                    'name': line.name,
                    'account_id': debit_account.id,
                    'debit': line.amount > 0.0 and line.amount or 0.0,
                    'credit': line.amount < 0.0 and -line.amount or 0.0, 
                    'partner_id': partner_id,
                    'journal_id': journal.id,
                    'date': account_date,
                    'analytic_account_id': line.analytic_account.id,

                })
                expense_line_ids.append(debit_line)
                credit_line = (0, 0, {#give
                    'name': line.name,
                    'account_id': line.credit_account.id,#employee_id.address_home_id.property_account_payable_id.id,
                    'debit': line.amount < 0.0 and -line.amount or 0.0,
                    'credit': line.amount > 0.0 and line.amount or 0.0, 
                    'partner_id': partner_id,
                    'journal_id': journal.id,
                    'date': account_date,
                    'analytic_account_id': line.analytic_account.id,

                })
                expense_line_ids.append(credit_line)
            move_value['line_ids'] = expense_line_ids
            move = self.env['account.move'].create(move_value)
            request.write({'move_id': move.id})
            move.post()
        return True"""
    