from odoo import models, fields, api

class CustomSale(models.Model):
    _name = 'custom.sale'
    _description = 'Custom Sale Model'

    name = fields.Char(string='Sale Name', required=True)
    product_ids = fields.Many2many('product.product', string='Products')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)

    @api.depends('product_ids.price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(product.price for product in record.product_ids)

class HidePriceZeroLine(models.Model):
    _name = 'hide.price.zero.line'
    _description = 'Hide Price Zero Line Model'

    sale_id = fields.Many2one('custom.sale', string='Sale Reference')
    product_id = fields.Many2one('product.product', string='Product')
    price = fields.Float(string='Price')

    @api.model
    def create(self, vals):
        if vals.get('price', 0.0) == 0.0:
            return super(HidePriceZeroLine, self).create(vals)
        else:
            return False  # Prevent creation if price is not zero