{
    'name': "Test Vehicle",
    'summary': "This is an online garage sysyem",
    'description': """This is an online garage sysyem
    """,
    'author': "Haileleul",
    'category': "Service",
    'sequence': -100,
    # 'version': "1.0.1",
    'depends': ['mail', 'base'],
    'data': [
        "security/ir.model.access.csv",
        "data/ir.sequence.xml",
        "data/vehicle_brands.xml",
        "data/vehicle_parts.xml",
        "views/driver_information.xml",
        "views/vehicle_brands.xml",
        "views/vehicle_parts.xml",
        "views/menu.xml",
    ],
    "demo": [],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}

# [options]
# admin_passwd = admin
# db_host = localhost
# db_port = 5432
# db_user = odoo
# db_password = admin
# addons_path = E:\OdooProject\odoo17\addons,E:\OdooProject\odoo-18.0\addons,E:\OdooProject\custom_addons
# http_port = 8069
# default_productivity_apps = True
