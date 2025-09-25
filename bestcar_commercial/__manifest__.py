# -*- coding: utf-8 -*-
{
    'name': "bestcar_commercial",

    'summary': "Commercial Management of a car dealer",

    'description': """
Long description of module's purpose
    """,

    'author': "Farid,Lorenzo,Jean-Marc",
    'license': "LGPL-3",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale_management', 'project', 'hr', 'purchase', 'stock', 'account'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/brand_data.xml',
        'data/model_data.xml',
        'data/department_data.xml',
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
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    "application": True,
    "sequence": -100,
}
