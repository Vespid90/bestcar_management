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
    is_vehicle = fields.Boolean(string="Is vehicle?")
    sale_ok = fields.Boolean(default=True)
    purchase_ok = fields.Boolean(default=True)

    is_storable = fields.Boolean(default=True)

    body_color = fields.Char(string="Color")
    emissions_standard = fields.Char(string="Emission Standard")
    class_of_emission = fields.Char(string="Class of emission")
    consumption = fields.Char(string="consumption")
    license_plate = fields.Char(string="License Plate")
    name = fields.Char(string="Name", compute='_compute_vehicle_name',store=True,readonly=True) #conca marque / model /  5 nb du vin(?)
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
    stock_time_days = fields.Float(string="Stock Time (days)")
    width_mm = fields.Float(string="Width (mm)")

    cylinders = fields.Integer(string="Number of Cylinders")
    doors = fields.Integer(string="Number of Doors")
    engine_capacity_cc = fields.Integer(string="Engine Capacity (cc)")
    horsepower_hp = fields.Integer(string="Horsepower (HP)")
    mileage_km = fields.Integer(string="Mileage (km)")
    warranty_km = fields.Integer(string="Warranty (km)")
    fiscal_power_cv = fields.Integer(string="Fiscal Power (CV)")

    image = fields.Image(string=" ",max_width=200, max_height=200)

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

    # Connect the vehicle to a warehouse location
    # location_id = fields.Many2one("stock.location", string="Stock Location")

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

    @api.depends('vehicle_brand_id','vehicle_model_id','vehicle_version','vin')
    def _compute_vehicle_name(self):
        for rec in self:
            if not rec.vehicle_brand_id.name or not rec.vehicle_model_id.name or not rec.vehicle_version or not rec.vin:
                rec.name = "New Vehicle"
            else:
                rec.name = f"{rec.vehicle_brand_id.name}-{rec.vehicle_model_id.name}-{rec.vehicle_version}-{(rec.vin or '')[:5]}"

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals["name"] = "New Vehicle"
        result = super(ProductTemplate, self).create(vals_list)
        for product in result:
            if product.is_vehicle:
                department = self.env['hr.department'].search([('name', '=', 'Mechanical Workshop')], limit=1)
                project = self.env['project.project'].create({
                            'active': True,
                            'name': f"{product.name} Reconditioning",
                            'user_id' : department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id,
                            'vehicle_id' : product.id,
                })
                stages_to_create = []
                for stage in PROJECT_STAGES:
                    stages_to_create.append({
                        'name': stage['name'],
                        'sequence': stage['sequence'],
                        'project_ids': [(4, project.id)],
                    })
                self.env['project.task.type'].create(stages_to_create)
                # inspection_task = self.env['project.task'].create({
                #     'name': f"{product.name} Inspection",
                #     'project_id': project.id,
                #     'priority': '1'
                # })
                self.env['project.task'].create([
                    {'name': f"{product.name} Inspection",'project_id': project.id,'user_ids': [(6,0,[department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id])],'priority': '1' },
                    {'name': f"{product.name} Repair",'project_id': project.id,'user_ids': [(6,0,[department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id])] },
                    {'name': f"{product.name} Maintenance",'project_id': project.id,'user_ids': [(6,0,[department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id])] },
                    {'name': f"{product.name} Cleaning",'project_id': project.id,'user_ids': [(6,0,[department.manager_id.user_id.id if department.manager_id.user_id else self.env.user.id])] }
                ])
        return result

    def button_buy(self):
        self.ensure_one()

        product_variant = self.product_variant_id

        return {
            "name":"Buy a vehicle",
            "type":"ir.actions.act_window",
            "res_model":"purchase.order",
            "view_mode":"form",
            "target":"current",
            "context":{
                "default_order_line":[(0, 0, {
                    "product_id":product_variant.id,
                    "name":product_variant.display_name,
                    "product_qty": 1.0,
                    "product_uom": product_variant.uom_id.id,
                })]
            }
        }

    def button_sale(self):
        self.ensure_one()

        product_variant = self.product_variant_id

        return {
            "name":"Sell a vehicle",
            "type":"ir.actions.act_window",
            "res_model":"sale.order",
            "view_mode":"form",
            "target":"current",
            "context":{
                "default_order_line":[(0, 0, {
                    "product_id":product_variant.id,
                    "name":product_variant.display_name,
                    "product_uom_qty": 1.0,
                    "product_uom": product_variant.uom_id.id,
                })]
            }
        }
