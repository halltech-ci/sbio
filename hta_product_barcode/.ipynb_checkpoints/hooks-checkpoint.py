# -*- coding: utf-8 -*-

def post_init_hook(cr, registry):
    cr.execute(
        """
    INSERT INTO product_barcode
    (product_id, product_tmpl_id, name, sequence)
    SELECT id, product_tmpl_id, barcode, 0
    FROM product_product
    WHERE barcode IS NOT NULL"""