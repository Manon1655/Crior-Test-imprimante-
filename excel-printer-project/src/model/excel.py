# -*- coding: utf-8 -*-
import io
import xlsxwriter
from odoo.exceptions import UserError  # type: ignore
from impression_brother_cmd import print_postes_with_cut
from printer.escp import send_to_printer  # Import the function to send data to the printer

class Writer:
    def __init__(self, order, config, env, lines):
        self.env = env
        self.config = config
        self.order = order
        self.lines = lines
        self.sections = []  # Storage for printing by post

        output = io.BytesIO()
        self.workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        self.worksheet = self.workbook.add_worksheet()

        self.lastRow = 0
        self._init_formats()
        self._writeHeader()

        postes_utilises = self._getWorkcenters()
        envoi = None

        for poste in sorted(postes_utilises, key=lambda p: p.name):
            if poste.name == 'Envoi':
                envoi = poste
                continue
            self._writeForPost(poste.name, poste)

        if envoi:
            self._writeForPost('Envoi', envoi)

        self._write_product('Serviette cocktail', "main", self.order.x_studio_nbre_de_convives + 10 or 0, 'UNITES')
        self._write_product('Gobelet petit', "main", self.order.x_studio_nbre_de_convives + 1 or 0, 'UNITES')
        self._write_product('Gobelet grand', "main", self.order.x_studio_nbre_de_convives + 1 or 0, 'UNITES')

        self.workbook.close()
        output.seek(0)
        self.file_data = output.read()

        # Print each section by post with automatic cutting
        try:
            for section in self.sections:
                post_name, content = section
                send_to_printer(content)  # Send content to printer
        except Exception as e:
            raise UserError(f"Erreur d'impression : {e}")

    # All other methods (_getWorkcenters, _init_formats, _writeHeader, etc.) remain unchanged

    def _writeForPost(self, post_name, post):
        contenu = []
        self.worksheet.write(self.lastRow, 0, '=B2', self.formats["left"])
        self.worksheet.write(self.lastRow + 1, 0, '=B4', self.formats["left"])
        self.worksheet.write(self.lastRow + 2, 0, '=A1', self.formats["left"])
        self.worksheet.write(self.lastRow + 2, 1, '=B3', self.formats["date2"])
        self.worksheet.write(self.lastRow + 2, 2, post_name, self.formats["post"])
        self.worksheet.write(self.lastRow + 3, 0, '=D3&" Pax"', self.formats["left"])
        self.worksheet.write(self.lastRow + 3, 2, '=D4', self.formats["post"])
        self.lastRow += 4

        for line in self.lines:
            product = line.product_id
            if not product or not product.name:
                continue

            name_written = False

            for component_info in self._get_all_components_with_qty(product, line.product_uom_qty):
                component = component_info['product']
                level = component_info['level']
                indent = '    ' * level
                name = f"{indent}- {component_info['name']}"

                productions = self.env['mrp.production'].search([
                    ('product_id', '=', component.id),
                    ('state', '!=', 'cancel')
                ])
                has_production_in_post = any(
                    post in p.workorder_ids.mapped('workcenter_id') for p in productions
                )

                if not has_production_in_post:
                    component_bom = self._get_bom(component)
                    if component_bom and component_bom.operation_ids:
                        if post in component_bom.operation_ids.mapped('workcenter_id'):
                            has_production_in_post = True

                if has_production_in_post:
                    if not name_written:
                        self.lastRow += 1
                        self._write_product(product.name, "main", line.product_uom_qty or 0, 'UNITES')
                        contenu.append(f"{product.name} : {line.product_uom_qty or 0} UNITES")
                        name_written = True

                    self._write_product(name, "comp", component_info['qty'], component_info['uom'])
                    contenu.append(f"{name.strip()} : {component_info['qty']} {component_info['uom']}")

            if not name_written:
                productions = self.env['mrp.production'].search([
                    ('product_id', '=', product.id),
                    ('state', '!=', 'cancel')
                ])
                has_production_in_post = any(
                    post in p.workorder_ids.mapped('workcenter_id') for p in productions
                )

                if not has_production_in_post:
                    bom = self._get_bom(product)
                    if bom and bom.operation_ids:
                        if post in bom.operation_ids.mapped('workcenter_id'):
                            has_production_in_post = True

                if has_production_in_post:
                    self._write_product(product.name, "main", line.product_uom_qty or 0, 'UNITES')
                    contenu.append(f"{product.name} : {line.product_uom_qty or 0} UNITES")

        if contenu:
            self.sections.append((post_name, "\n".join(contenu)))

        if post_name != 'Envoi':
            self.lastRow += 2