from odoo import fields, models

class Vehicle(models.Model):
    _name = "vehicle.vehicle"
    _description = "Vehicle"
    _inherits = {"product.product": "product_id"}

    # Boolean
    is_rental = fields.Boolean(string="Rental YES / NO")
    is_used = fields.Boolean(string="Used YES / NO")

    # Char
    body_color = fields.Char(string="Color")
    emissions_standard = fields.Char(string="Emission Standard")
    license_plate = fields.Char(string="License Plate")
    _sql_constraints = [
        (
            "unique_license_plate",
            "unique(license_plate)",
            "The license plate must be unique for each vehicle.",
        ),
    ]
    reference_number = fields.Char(string="Reference Number")
    vin = fields.Char(string="VIN")
    _sql_constraints = [
        ('vin_number_unique', 'unique(vin)', "The VIN must be unique!")
    ]
    vehicle_brand = fields.Char(string="Brand")
    vehicle_model = fields.Char(string="Model")
    vehicle_version = fields.Char(string="Version")

    # Date
    date_arrival = fields.Date(string="Arrival Date")
    date_first_registration = fields.Date(string="First Registration Date")
    date_purchase = fields.Date(string="Purchase Date")
    date_sale = fields.Date(string="Sale Date")

    # Float
    co2_g_km = fields.Float(string="CO₂ Emission (g/km)")
    fuel_tank_volume_l = fields.Float(string="Fuel Tank Volume (L)")
    gross_weight_kg = fields.Float(string="Gross Weight (kg)")
    height_mm = fields.Float(string="Height (mm)")
    kerb_weight_kg = fields.Float(string="Kerb Weight (kg)")
    length_mm = fields.Float(string="Length (mm)")
    stock_time_days = fields.Float(string="Stock Time (days)")
    width_mm = fields.Float(string="Width (mm)")

    # Integer
    cylinders = fields.Integer(string="Number of Cylinders")
    doors = fields.Integer(string="Number of Doors")
    engine_capacity_cc = fields.Integer(string="Engine Capacity (cc)")
    horsepower_hp = fields.Integer(string="Horsepower (HP)")
    mileage_km = fields.Integer(string="Mileage (km)")
    warranty_km = fields.Integer(string="Warranty (km)")
    fiscal_power_cv = fields.Integer(string="Fiscal Power (CV)")

    # Monetary
    purchase_price = fields.Monetary(string="Purchase Price", currency_field="currency_id")

    # Selection
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
    status = fields.Selection(
        [
            ("added", "File Added"),
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
    vehicle_type = fields.Selection(
        [
            ("sedan", "Sedan"),
            ("station_wagon", "Station Wagon"),
            ("suv", "SUV"),
            ("city_car", "City Car"),
            ("coupe", "Coupe"),
            ("convertible", "Convertible"),
            ("minivan", "Minivan"),
            ("van", "Van"),
            ("pick_up", "Pick-up"),
            ("other", "Other"),
        ],
        string="Vehicle Type",
    )

    # Link each vehicle to a product.product record
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        ondelete="cascade",
    )

    # Connect the vehicle to the country of origin
    country_of_origin_id = fields.Many2one("res.country", string="Country of Origin")

    #Specify the currency for the purchase_price field. By default, it assumes the company currency
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id.id,
        required=True,
    )

    # Connect the vehicle to a warehouse location
    location_id = fields.Many2one("stock.location", string="Stock Location")

    # Connect the vehicle to a supplier
    supplier_id = fields.Many2one(
        "res.partner",
        string="Supplier",
        domain="[('supplier_rank','>',0)]",
    )

    # Connect the vehicle to a list of configurable options
    option_line_ids = fields.One2many(
        "vehicle.option",
        "vehicle_id",
        string="Options (name + value)",
    )











