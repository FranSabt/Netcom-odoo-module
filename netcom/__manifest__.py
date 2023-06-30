# -*- coding: utf-8 -*-
# More info at https://www.odoo.com/documentation/master/reference/module.html

{
    "name": "Netcom",
    "category": 'Human Resources',
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",

        "views/netcom_views.xml",
        "views/departamentos.xml",
        "views/netcom_menus.xml",

    ],
    "application": True,
}
