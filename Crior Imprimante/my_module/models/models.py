from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CustomSale(models.Model):
    """
    Représente une vente personnalisée liée à plusieurs produits.
    Le montant total est calculé automatiquement à partir des prix des produits.
    """
    _name = 'custom.sale'
    _description = 'Custom Sale'

    name = fields.Char(string='Sale Name', required=True)
    product_ids = fields.Many2many('product.product', string='Products')
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True
    )

    @api.depends('product_ids.lst_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(product.lst_price for product in record.product_ids)


class HidePriceZeroLine(models.Model):
    """
    Représente une ligne de produit avec un prix nul,
    liée à une vente personnalisée.
    """
    _name = 'hide.price.zero.line'
    _description = 'Hide Price Zero Line'

    sale_id = fields.Many2one(
        'custom.sale',
        string='Sale Reference',
        required=True,
        ondelete='cascade'
    )
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )
    price = fields.Float(string='Price', required=True)

    @api.model
    def create(self, vals):
        if vals.get('price', 0.0) == 0.0:
            return super().create(vals)
        raise ValidationError("Only lines with a price of 0.0 can be created.")
