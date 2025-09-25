from odoo import models, fields, api

PROJECT_STAGES = [
    {'name': 'New', 'sequence': 1},
    {'name': 'In Progress', 'sequence': 2},
    {'name': 'Done', 'sequence': 3},
    {'name': 'Cancelled', 'sequence': 4}
]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    active = fields.Boolean(default=True)
    is_used = fields.Boolean(string="Is used ?")
    is_trade_in = fields.Boolean(string="Is trade-in?")
    trade_in = fields.Boolean(string="Trade-in")
    is_vehicle = fields.Boolean(string="Is vehicle?")
    sale_ok = fields.Boolean(default=True)
    purchase_ok = fields.Boolean(default=True)

    is_storable = fields.Boolean(default=True)

    body_color = fields.Char(string="Color")
    emissions_standard = fields.Char(string="Emission Standard")
    class_of_emission = fields.Char(string="Class of emission")
    consumption = fields.Char(string="consumption")
    license_plate = fields.Char(string="License Plate")
    name = fields.Char(string="Name", compute='_compute_vehicle_name', store=True, readonly=True,
                       default='New Vehicle')  # conca marque / model /  5 nb du vin(?)
    reference_number = fields.Char(string="Reference Number")  # unique VN = 1 / VO = 2 / année / number incrémenté
    vehicle_model = fields.Char(string="Model")
    vehicle_version = fields.Char(string="Version")
    vin = fields.Char(string="VIN")

    date_arrival = fields.Date(string="Arrival Date", readonly=True)
    date_first_registration = fields.Date(string="First Registration Date")
    date_purchase = fields.Date(string="Purchase Date", readonly=True)
    date_sale = fields.Date(string="Sale Date", readonly=True)

    co2_g_km = fields.Float(string="CO₂ Emission (g/km)")
    fuel_tank_volume_l = fields.Float(string="Fuel Tank Volume (L)")
    gross_weight_kg = fields.Float(string="Gross Weight (kg)")
    height_mm = fields.Float(string="Height (mm)")
    kerb_weight_kg = fields.Float(string="Kerb Weight (kg)")
    length_mm = fields.Float(string="Length (mm)")
    stock_time_days = fields.Float(string="Stock Time (days)", compute="_compute_stock_time", store=True)
    width_mm = fields.Float(string="Width (mm)")

    cylinders = fields.Integer(string="Number of Cylinders")
    doors = fields.Integer(string="Number of Doors")
    engine_capacity_cc = fields.Integer(string="Engine Capacity (cc)")
    horsepower_hp = fields.Integer(string="Horsepower (HP)")
    mileage_km = fields.Integer(string="Mileage (km)")
    warranty_km = fields.Integer(string="Warranty (km)")
    fiscal_power_cv = fields.Integer(string="Fiscal Power (CV)")

    image = fields.Image(string=" ", max_width=200, max_height=200)

    purchase_price = fields.Monetary(string="Purchase Price", currency_field="currency_id")

    _sql_constraints = [
        (
            "unique_license_plate",
            "unique(license_plate)",
            "The license plate must be unique for each vehicle.",
        ),
        ('vin_number_unique', 'unique(vin)', "The VIN must be unique!")

    ]

    energy_type = fields.Selection(
        [
            ("petrol", "Petrol"),
            ("diesel", "Diesel"),
            ("hybrid", "Hybrid"),
            ("electric", "Electric"),
        ],
        string="Energy Type",
    )
    gearbox = fields.Selection(
        [("auto", "Automatic"), ("man", "Manual")],
        string="Gearbox",
    )

    status = fields.Selection(
        [
            ("added", "Vehicle Added"),
            ("waiting_arrival", "Waiting for Arrival"),
            ("reconditioning", "In Reconditioning"),
            ("for_sale", "For Sale"),
            ("reserved", "Reserved"),
            ("payment", "In Payment"),
            ("waiting_TI", "Waiting Technical Inspection"),
            ("waiting_delivery", "Waiting for Delivery"),
            ("delivered", "Delivered"),
        ],
        string="Status",
        default="added",
    )

    currency_id = fields.Many2one("res.currency",
                                  string="Currency",
                                  default=lambda self: self.env.company.currency_id.id,
                                  )

    country_of_origin_id = fields.Many2one("res.country", string="Country of Origin")
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company.id,
    )

    supplier_id = fields.Many2one(
        "res.partner",
        string="Supplier",
    )

    vehicle_brand_id = fields.Many2one(comodel_name="vehicle.brand", string="Make")
    vehicle_model_id = fields.Many2one(comodel_name="vehicle.model",
                                       domain="[('brand_id', '=', vehicle_brand_id)]")
    vehicle_type_id = fields.Many2one(comodel_name="vehicle.type",
                                      string="Type",
                                      related="vehicle_model_id.type_id",
                                      readonly=True)
    project_ids = fields.One2many(comodel_name="project.project",
                                  inverse_name="vehicle_id",
                                  string="Projects")

    def _default_uom_id(self):
        return self.env.ref("uom.product_uom_unit", raise_if_not_found=False).id

    def _default_categ_id(self):
        return self.env.ref("product.product_category_all", raise_if_not_found=False).id

    uom_id = fields.Many2one("uom.uom", string="Unit of measure",
                             default=_default_uom_id)
    uom_po_id = fields.Many2one("uom.uom", string="Purchase Unit of Measure",
                                default=_default_uom_id)
    categ_id = fields.Many2one("product.category", string="Category",
                               default=_default_categ_id)

    @api.depends('vehicle_brand_id', 'vehicle_model_id', 'vehicle_version', 'vin')
    def _compute_vehicle_name(self):
        for rec in self:
            if not rec.vehicle_brand_id.name or not rec.vehicle_model_id.name or not rec.vehicle_version or not rec.vin:
                base_name = "New Vehicle"
            else:
                base_name = f"{rec.vehicle_brand_id.name}-{rec.vehicle_model_id.name}-{rec.vehicle_version}-{(rec.vin or '')[0:3]}{(rec.vin or '')[12:17]}"

            if rec.trade_in:
                rec.name = f"TRD - {base_name}"
            else:
                rec.name = base_name

    @api.depends('date_arrival', 'date_sale')
    def _compute_stock_time(self):
        for rec in self:
            if rec.date_arrival:
                if not rec.date_sale:
                    rec.stock_time_days = (fields.Date.today() - rec.date_arrival).days
                else:
                    rec.stock_time_days = (rec.date_sale - rec.date_arrival).days


    @api.model_create_multi
    def create(self, vals_list):
        """

        Used to generate a product.template for vehicle trade-ins (trade-in) + a different VIN (unique car) which ends with '-TRD'

        """
        records = super().create(vals_list)

        for rec, vals in zip(records, vals_list):
            if vals.get("is_trade_in"):

                vin = rec.vin or ""
                if not vin.endswith("-TRD"):
                    vin = f"{vin}-TRD"

                trade_in_vals = {
                    "trade_in": True,
                    "name": rec.name,
                    "purchase_price": rec.purchase_price,
                    "type": 'service',
                    "vehicle_brand_id": rec.vehicle_brand_id.id,
                    "vehicle_model_id": rec.vehicle_model_id.id,
                    "vehicle_version": rec.vehicle_version,
                    "vin": vin,
                    "list_price": -abs(rec.purchase_price),
                    "is_vehicle": rec.is_vehicle,
                }

                self.create(trade_in_vals)

        return records

    def button_buy(self):
        self.ensure_one()

        product_variant = self.product_variant_id

        return {
            "name": "Buy a vehicle",
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_order_line": [(0, 0, {
                    "product_id": product_variant.id,
                    "name": product_variant.display_name,
                    "product_qty": 1.0,
                    "product_uom": product_variant.uom_id.id,
                })],
            }
        }

    def button_sale(self):
        self.ensure_one()

        product_variant = self.product_variant_id

        return {
            "name": "Sell a vehicle",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": "form",
            "target": "current",
            "context": {
                "default_order_line": [(0, 0, {
                    "product_id": product_variant.id,
                    "name": product_variant.display_name,
                    "product_uom_qty": 1.0,
                    "product_uom": product_variant.uom_id.id,
                })],
            }
        }

    def button_ready(self):
        for rec in self:
            rec.status = 'for_sale'

    def button_TI(self):
        for rec in self:
            rec.status = 'waiting_delivery'
