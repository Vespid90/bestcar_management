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
    is_used = fields.Boolean(string="Used vehicle")
    sale_ok = fields.Boolean(default=True)
    purchase_ok = fields.Boolean(default=True)

    body_color = fields.Char(string="Color")
    emissions_standard = fields.Char(string="Emission Standard")
    license_plate = fields.Char(string="License Plate")
    name = fields.Char(string="Name", default="Vehicle") #conca marque / model /  4 nb du vin(?)
    reference_number = fields.Char(string="Reference Number") #unique VN = 1 / VO = 2 / année / number incrémenté
    vehicle_model = fields.Char(string="Model")
    vehicle_version = fields.Char(string="Version")
    vin = fields.Char(string="VIN")

    date_arrival = fields.Date(string="Arrival Date")
    date_first_registration = fields.Date(string="First Registration Date")
    date_purchase = fields.Date(string="Purchase Date")
    date_sale = fields.Date(string="Sale Date")

    co2_g_km = fields.Float(string="CO₂ Emission (g/km)")
    fuel_tank_volume_l = fields.Float(string="Fuel Tank Volume (L)")
    gross_weight_kg = fields.Float(string="Gross Weight (kg)")
    height_mm = fields.Float(string="Height (mm)")
    kerb_weight_kg = fields.Float(string="Kerb Weight (kg)")
    length_mm = fields.Float(string="Length (mm)")
    list_price = fields.Float(default=0.0)
    stock_time_days = fields.Float(string="Stock Time (days)")
    width_mm = fields.Float(string="Width (mm)")

    cylinders = fields.Integer(string="Number of Cylinders")
    doors = fields.Integer(string="Number of Doors")
    engine_capacity_cc = fields.Integer(string="Engine Capacity (cc)")
    horsepower_hp = fields.Integer(string="Horsepower (HP)")
    mileage_km = fields.Integer(string="Mileage (km)")
    warranty_km = fields.Integer(string="Warranty (km)")
    fiscal_power_cv = fields.Integer(string="Fiscal Power (CV)")

    image = fields.Image("Logo", max_width=128, max_height=128)

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
    nature = fields.Selection(
        [("new", "New"), ("used", "Used"), ("demo", "Demo")],
        string="Vehicle Nature",
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

    # Connect the vehicle to a warehouse location
    # location_id = fields.Many2one("stock.location", string="Stock Location")

    supplier_id = fields.Many2one(
        "res.partner",
        string="Supplier",
    )

    vehicle_brand_id = fields.Many2one(comodel_name="vehicle.brand", string="Brand")
    vehicle_model_id = fields.Many2one(comodel_name="vehicle.model", string="Model",
                                       domain="[('brand_id', '=', vehicle_brand_id)]")
    vehicle_type_id = fields.Many2one(comodel_name="vehicle.type",
                                      string="Type",
                                      related="vehicle_model_id.type_id",
                                      readonly=True)

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
    # status = fields.Selection(
    #     [
    #         ("added", "File Added"),
    #         ("waiting_arrival", "Waiting for Arrival"),
    #         ("reconditioning", "In Reconditioning"),
    #         ("for_sale", "For Sale"),
    #         ("reserved", "Reserved"),
    #         ("payment", "In Payment"),
    #         ("waiting_delivery", "Waiting for Delivery"),
    #         ("delivered", "Delivered"),
    #     ],
    #     string="Status",
    #     default="added",
    # )
    @api.model_create_multi
    def create(self,vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        if templates:
            product = templates[0]
            project = self.env['project.project'].create({
                        'active': True,
                        'name': f"{product.name} Reconditioning",
                        'allow_task_dependencies': True
            })
            stages_to_create = []
            for stage in PROJECT_STAGES:
                stages_to_create.append({
                    'name': stage['name'],
                    'sequence': stage['sequence'],
                    'project_ids': [(4, project.id)],  # link stage to project
                })
            self.env['project.task.type'].create(stages_to_create)

            inspection_task = self.env['project.task'].create({
                'name': f"{product.name} Inspection",
                'project_id': project.id,
                'priority': '1'
            })
            print(inspection_task.id)

            self.env['project.task'].create([
                {'name': f"{product.name} Repair",'project_id': project.id, 'depend_on_ids': [(4, inspection_task.id)]},
                {'name': f"{product.name} Maintenance",'project_id': project.id, 'depend_on_ids':[(4, inspection_task.id)]},
                {'name': f"{product.name} Cleaning",'project_id': project.id, 'depend_on_ids': [(4, inspection_task.id)]}
              ])


        return templates
