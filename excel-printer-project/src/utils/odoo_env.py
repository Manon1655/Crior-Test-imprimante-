from odoo import api, SUPERUSER_ID

def get_order(env, order_id):
    return env['sale.order'].browse(order_id)

def get_order_lines(env, order):
    return order.order_line

def get_workcenters(env):
    return env['mrp.workcenter'].search([])

def get_bom(env, product):
    return env['mrp.bom'].search([('product_tmpl_id', '=', product.product_tmpl_id.id)], limit=1)

def get_production(env, product):
    return env['mrp.production'].search([('product_id', '=', product.id), ('state', '!=', 'cancel')])