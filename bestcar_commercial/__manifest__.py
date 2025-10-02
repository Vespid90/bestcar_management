# -*- coding: utf-8 -*-
{
    'name': "Bestcar commercial",

    'summary': "Commercial Management of a car dealer",

    'description':
    """
    BestCar Commercial Management
    
    This module allows managing the commercial activity of a car dealership specializing in the resale of used vehicles. 
    It includes the following features:
    
    - Used vehicle management: tracking technical information, brand, model, type, and condition of vehicles.
    - Trade-in system: ability to record and manage vehicles taken in as trade-ins by the dealership.
    - Customer management: tracking contacts, purchase history, and trade-ins.
    - Integration with purchase and sales orders to ensure a complete commercial workflow.
    - Automatic creation of tasks related to vehicles (maintenance, inspection, preparation for sale).
    - Integration with standard Odoo modules (project, stock, purchase, sales, human resources).
    
    Objective: provide a complete and easy-to-use tool to manage the resale of used vehicles while keeping a clear overview of operational tasks and trade-ins.    
    """,

    'author': "Farid Elmam,Lorenzo Mignini,Jean-Marc Broutin",
    'license': "LGPL-3",
    'category': 'Uncategorized',
    'version': '18.0.0.1',
    'depends': ['base', 'product', 'sale_management', 'project', 'hr', 'purchase', 'stock', 'l10n_be'],

    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/hr_data.xml',
        'data/stock_data.xml',
        'data/brand_data.xml',
        'data/model_data.xml',
        'views/res_partner_views.xml',
        'views/vehicle_menu.xml',
        'views/product_template.xml',
        'views/vehicle_brand_views.xml',
        'views/vehicle_model_views.xml',
        'views/vehicle_type_views.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'reports/vehicle_report.xml',
        'reports/vehicle_templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    "application": True,
    "sequence": -100,
}
