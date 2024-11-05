{
    'name': "Test Vehicle",
    'summary': "This is an online garage sysyem",
    'description': """This is an online garage sysyem
    """,
    'author': "Haileleul",
    'category': "Service",
    'sequence': -100,
    'version': "1.0.1",
    'depends': ['mail', 'base'],
    'data': [
        # groups
        "security/ir.model.access.csv",

        # data
        "data/ir.sequence.xml",
        "data/vehicle_brands.xml",
        "data/vehicle_parts.xml",
        "data/required_checkups.xml",
        "data/inspection_types.xml",
        "data/maintenance_types.xml",
        "data/service_types.xml",

        # views
        "views/driver_information.xml",
        "views/vehicle_brands.xml",
        "views/vehicle_parts.xml",
        "views/vehicle_services.xml",

         # test
        "views/check.xml",
        "views/service.xml",
        "views/inspection.xml",
        "views/maintenance.xml",
        "views/menu.xml",
    ],
    "demo": [],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}

