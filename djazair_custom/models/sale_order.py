from odoo import models, fields, api

_wilayas = [
    ("1", "Adrar"),
    ("2", "Chlef"),
    ("3", "Laghouat"),
    ("4", "Oum El Bouaghi"),
    ("5", "Batna"),
    ("6", "Béjaïa"),
    ("7", "Biskra"),
    ("8", "Béchar"),
    ("9", "Blida"),
    ("10", "Bouira"),
    ("11", "Tamanrasset"),
    ("12", "Tébessa"),
    ("13", "Tlemcen"),
    ("14", "Tiaret"),
    ("15", "Tizi Ouzou"),
    ("16", "Alger"),
    ("17", "Djelfa"),
    ("18", "Jijel"),
    ("19", "Sétif"),
    ("20", "Saïda"),
    ("21", "Skikda"),
    ("22", "Sidi Bel Abbès"),
    ("23", "Annaba"),
    ("24", "Guelma"),
    ("25", "Constantine"),
    ("26", "Médéa"),
    ("27", "Mostaganem"),
    ("28", "M'Sila"),
    ("29", "Mascara"),
    ("30", "Ouargla"),
    ("31", "Oran"),
    ("32", "El Bayadh"),
    ("33", "Illizi"),
    ("34", "Bordj Bou Arréridj"),
    ("35", "Boumerdès"),
    ("36", "El Tarf"),
    ("37", "Tindouf"),
    ("38", "Tissemsilt"),
    ("39", "El Oued"),
    ("40", "Khenchela"),
    ("41", "Souk Ahras"),
    ("42", "Tipaza"),
    ("43", "Mila"),
    ("44", "Aïn Defla"),
    ("45", "Naâma"),
    ("46", "Aïn Témouchent"),
    ("47", "Ghardaïa"),
    ("48", "Relizane"),
    ("49", "Timimoun"),
    ("50", "Bordj Badji Mokhtar"),
    ("51", "Ouled Djellal"),
    ("52", "Béni Abbès"),
    ("53", "In Salah"),
    ("54", "In Guezzam"),
    ("55", "Touggourt"),
    ("56", "Djanet"),
    ("57", "El M'Ghair"),
    ("58", "El Meniaa"),
    ("59", "Aflou"),
    ("60","Brikcha"),
    ("61", "El Kantara"),
    ("62", "Bir El Ater"),
    ("63", "El Aricha"),
    ("64", "Ksar Chellala"),
    ("65", "Aïn Oussera"),
    ("66", "Messaad"),
    ("67", "Ksar El Boukhari"),
    ("68", "Bou Saâda"),
    ("69", "El Abiodh Sidi Cheikh")
]

class SaleOrder(models.Model):
    _inherit="sale.order"

    wilaya=fields.Selection(_wilayas,string="Destination Wilaya", required=True, default="16")

    shipping_estimate = fields.Monetary(
        string="Estimated Shipping",
        compute="_compute_shipping_estimate",
        currency_field="currency_id"
    )

    @api.depends("wilaya")
    def _compute_shipping_estimate(self):
        for rec in self:
            if rec.wilaya == "16":
                rec.shipping_estimate=5000.0
            elif rec.wilaya == "31":
                rec.shipping_estimate=6000.0
            elif rec.wilaya == "01":
                rec.shipping_estimate=0.0
            else:
                rec.shipping_estimate=2000.0
    
    def action_apply_shipping(self):
        for rec in self:
            if rec.shipping_estimate <= 0:
                continue # do nothing if free
            else:
                shipping_product = self.env["product.product"].search([("name","=","Shipping Fees")],limit=1)

                if not shipping_product:
                    raise ValidationError("Please create a 'Shipping Fees' product first!")
                
                rec.write({
                    "order_line":[(0,0,{
                        "product_id":shipping_product.id,
                        "name":"Delivery to " + dict(rec._fields['wilaya'].selection).get(rec.wilaya),
                        "product_uom_qty":1,
                        "price_unit":rec.shipping_estimate,
                        "tax_id":[(6,0,shipping_product.taxes_id.ids)]
                    })]
                })