# -*- coding: utf-8 -*-
# More info at https://www.odoo.com/documentation/master/reference/module.html

{
    "name": "Controlador",
    "category": '',
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",

        "views/controlador_views.xml",
        "views/controlador_planes.xml",
        "views/controlador_routers.xml",
        "views/controlador_menus.xml",

    ],
    "application": True,
}
