{
    'name': "Test Vehicle",
    'summary': "This is an online garage sysyem",
    'description': """This is an online garage sysyem
    """,
    'author': "Haileleul",
    'category': 'Service',
    'sequence': -100,
    'version': "1.0.1",
    'depends': ['mail', 'base'],
    'data': [
        # groups
        "security/res.groups.xml",
        "security/ir.model.access.csv",

        # data
        "data/ir.sequence.xml",
        "data/vehicle_brands.xml",
        "data/vehicle_parts.xml",
        "data/required_checkups.xml",
        "data/inspection_types.xml",
        "data/maintenance_types.xml",
        "data/service_types.xml",
        "data/property_tag.xml",

        # views
        "views/driver_information.xml",
        "views/vehicle_brands.xml",
        "views/vehicle_information.xml",
        "views/vehicle_parts.xml",
        "views/vehicle_services.xml",
        "views/template.xml",

        # viwes
        "views/check.xml",
        "views/service.xml",
        "views/inspection.xml",
        "views/maintenance.xml",
        "views/stock.xml",
        "views/menu.xml",

        # report
        'report/report_template.xml',
        'report/vehicle_report.xml',
        'report/driver_report.xml',
    ],
    "demo": [],
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
