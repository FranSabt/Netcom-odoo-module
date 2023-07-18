# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

"""
El modulo no crea los Planess en la API.
Sino que verifica su existencia en en BD de Router y rellena los campos si este existe.
Evitamos de este modo que un usuario malicioso pueda llenar la BD con datos innecesarios.
"""

class Planes(models.Model):
    _name = 'plan'
    _description = "Lista de planes de Netcom Plus"
    _order = "id desc"
    _sql_constraints = [
        ("constrain_name", "UNIQUE(name)", "El \"Nombre Comercial\" debe ser unico."),
        ("constrain_groupname", "UNIQUE(groupame)", "El \"Nombre Lista\" debe ser unico."),
    ]

    #* Hay que colocar como name el nombre que uno desea que se refleje en la UI
    name = fields.Char("Nombre Comercial", required=True)
    groupname = fields.Char("Nombre Lista")
    description = fields.Text("Descripcion")



    # @api.depends("name", "goupname", "description")
    # def enviar_a_api(self):

    #     name = ""
    #     for record in self:
    #         name = record.name

    #     # Enviar los datos a la API
    #     url = 'http://localhost:3333/plan/name/' + name
    #     response = requests.get(url)

    #     # print(response)
    #     print("\n----------------", end="")
    #     print(response.status_code, end="")
    #     print("----------------\n")

    #     if response.status_code == 200 or response.status_code == 201:
    #         data = response.json()
    #         print(data)
    #         for record in self:
    #             record.id_API  = data["id"]
    #             record.nombre_lista = data["nombre_lista"]
    #             record.carga = data["carga"]
    #             record.descarga = data["descarga"]
    #             record.id_API = data["id"]
                

    #             if record.id_API and record.nombre_lista  and record.carga and record.descarga:
    #                 record.activo = True
    #             else:
    #                 raise ValidationError("Alguno de los campos esta faltando en la BD!")
    #     else:
    #         print("Oh no!")
    #         print(response.text)
    #         raise ValidationError("Oh no!")