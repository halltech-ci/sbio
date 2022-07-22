odoo.define('bi_pos_barcode_lot_selection.models', function(require) {
	"use strict";

	var PosDB = require('point_of_sale.DB');
	var models = require('point_of_sale.models');
	var core = require('web.core');	
	var QWeb = core.qweb;
	var _t = core._t;

	models.load_fields('product.product', ['type','barcode_ids','qty_available']);

	models.load_models({
		model:  'stock.production.lot',
		fields: ['name','product_id','product_tmpl_id','barcode',
			'lot_name','product_qty','expiry_date','expiration_date',
			'avail_locations','quant_text'],
		domain: function(self){return [['product_qty', '>', 0]];}, 
		loaded: function(self,barcode){
			let today = new Date();
			let dd = today.getDate();
			let mm = today.getMonth()+1; //January is 0!
			let yyyy = today.getFullYear();
			if(dd<10){dd='0'+dd;} 
			if(mm<10){mm='0'+mm;} 
			today = yyyy+'-'+mm+'-'+dd;

			let brcds = [];
			let location = false;
			let loc_type = self.config.show_stock_location;
			
			if(self.config.op_typ_loc_id ){
				location = self.config.op_typ_loc_id[0];
			}
			barcode.forEach(function(brcd) {
				let is_valid = brcd.avail_locations.indexOf(location);
				brcd.all_qty = JSON.parse(brcd.quant_text);
				if( location && loc_type == 'specific' && is_valid > -1 ){
					brcd.loc_qty = brcd.all_qty[location];
					if(brcd.expiry_date){
						if (brcd.expiry_date >= today){
							brcds.push(brcd);
						}
					}else{
						brcds.push(brcd);
					}
				}
				if(loc_type != 'specific'){
					if(brcd.expiry_date){
						if (brcd.expiry_date >= today){
							brcds.push(brcd);
						}
					}else{
						brcds.push(brcd);
					}
				}
			});
			self.lot_barcodes = brcds;
			self.db.add_barcode_lots(brcds,location,loc_type);
		},
	});

	PosDB.include({
		init: function(options){
			this._super(options);			
			this.lot_barcode_by_name = {};
			this.lot_barcode_by_id = {};
			this.lot_barcode_by_lotbrcd = {};	
			this.location = false;
			this.loc_type = false;
		},

		add_barcode_lots: function (barcode,location,loc_type) {
			var self = this;
			this.location = location;
			this.loc_type = loc_type;
			barcode.forEach(function(brcd) {
				self.lot_barcode_by_name[brcd.name] = brcd;
				self.lot_barcode_by_id[brcd.id] = brcd;
				self.lot_barcode_by_lotbrcd[brcd.lot_name] = brcd;
			});
		},

		get_lot_barcode_by_lotbrcd: function(lot_name){
			if(this.lot_barcode_by_lotbrcd[lot_name]){
				return this.lot_barcode_by_lotbrcd[lot_name];
			} else {
				return undefined;
			}
		},

		get_lot_barcode_by_name: function(name){
			if(this.lot_barcode_by_name[name]){
				return this.lot_barcode_by_name[name];
			} else {
				return undefined;
			}
		},

		get_lot_barcode_by_id: function(id){
			if(this.lot_barcode_by_id[id]){
				return this.lot_barcode_by_id[id];
			} else {
				return undefined;
			}
		},

		get_lot_barcode_by_prod_id(id){
			let self = this;
			let barcodes = this.lot_barcode_by_name;
			let brcd_lst = [];
			$.each(barcodes, function( i, line ){
				if(self.loc_type == 'specific'){
					if (line.product_id[0] == id && line.loc_qty > 0){
						brcd_lst.push(line)
					}
				}else{
					if (line.product_id[0] == id && line.product_qty > 0){
						brcd_lst.push(line)
					}
				}
			});
			return brcd_lst;
		},
	});

	var _super_posmodel = models.PosModel.prototype;
	models.PosModel = models.PosModel.extend({
		scan_product: function(parsed_code) {
			var self = this;
			var res = _super_posmodel.scan_product.apply(this,arguments);
			var selectedOrder = this.get_order();
			var barcode = self.db.get_lot_barcode_by_lotbrcd(parsed_code.base_code);
			if(barcode && barcode.product_id && barcode.lot_name){
				var product = self.db.get_product_by_id(barcode.product_id[0]);
				if(product){
//					let modifiedPackLotLines = {};
//					let newPackLotLines = [{lot_name: barcode.name}];
//					let draftPackLotLines = { modifiedPackLotLines, newPackLotLines };
//					selectedOrder.add_product(product, {draftPackLotLines,});
                    selectedOrder.add_product(product,{lot_name: barcode.name});
					return true;
				}
			}
			return res;
		},
	});

	var OrderlineSuper = models.Orderline.prototype;
	models.Orderline = models.Orderline.extend({

		initialize: function(attr, options) {
			this.lots = this.lots || [];
			this.lots_barcode = this.lots_barcode || [];
			OrderlineSuper.initialize.call(this,attr,options);
		},

		get_lot_barcodes : function () {
			return this.lots_barcode;
		},

		export_as_JSON: function() {
			var self = this;
			var json = OrderlineSuper.export_as_JSON.apply(this,arguments);
			var lots = [];
			var lot_brcd = [];

			$.each(self.pack_lot_lines.models, function( i, line ){
				lots.push(line.attributes.lot_name)
			});
			
			if(lots){
				let lot_barcodes = self.pos.lot_barcodes;
				$.each(lot_barcodes, function( i, line ){
					let is_valid = lots.indexOf(line.name);
					if(is_valid > -1 ){
						lot_brcd.push(line);
					}
				});
			}
			self.lots = lots;
			self.lots_barcode = lot_brcd || [];
			json.lots = lots|| [];
			json.lots_barcode = lot_brcd|| [];
			return json;
		},
		
		init_from_JSON: function(json){
			OrderlineSuper.init_from_JSON.apply(this,arguments);
			this.lots = json.lots;
			this.lots_barcode = this.lots_barcode || [];
		},

		export_for_printing: function() {
			var json = OrderlineSuper.export_for_printing.apply(this,arguments);
			json.lots = this.lots || [];
			json.lots_barcode = this.lots_barcode || [];
			return json;
		},

	});

});
