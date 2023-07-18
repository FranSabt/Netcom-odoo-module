# -*- coding: utf-8 -*-
# More info at https://www.odoo.com/documentation/master/reference/module.html

{
    "name": "Controlador",
    "category": 'conexion',
    "depends": [
        "base",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        #"security/controlador_security.xml",

        "views/controlador_cliente.xml",
        "views/controlador_nas.xml",
        "views/controlador_zona.xml",
        "views/controlador_plan.xml",
        "views/controlador_menus.xml",

    ],
    "application": True,
}
