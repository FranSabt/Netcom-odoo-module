# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

"""
El modulo no crea los Routers en la API.
Sino que verifica su existencia en en BD de Router y rellena los campos si este existe.
Evitamos de este modo que un usuario malicioso pueda llenar la BD con datos innecesarios.
"""

class Routers(models.Model):
    _name = 'routers'
    _description = "Lista de routers de Netcom Plus"
    _order = "id desc"
    _sql_constraints = [
        ("name", "UNIQUE(name)", "El \"Hostname\" debe ser unico."),
    ]

    #* Hay que colocar como name el nombre que uno desea que se refleje en la UI
    name = fields.Char("Hostname", required=True)
    usuario = fields.Char("Usuario", readonly=True)
    puerto_api = fields.Char("Puerto API", readonly=True)
    direccion_ip = fields.Char("Direccion IP", readonly=True)
    id_API = fields.Integer("id", readonly=True)
    valid = fields.Boolean("router valido",default=False, readonly=True)


    @api.depends("name", "usuario", "password", "hostname", "puerto_api")
    def enviar_a_api(self):

        # La variable contiene el valor en el campo name (self.name) y realizar la busqueda en BD.
        name = "" 
        for record in self:
            name = record.name
            print(record.name)

        # Enviar los datos a la API
        url = 'http://localhost:3333/router/name/' + name
        response = requests.get(url)

        print("\n----------------", end="")
        print(response.status_code, end="")
        print("----------------\n")

        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            print(data)
            for record in self:
                record.id_API  = data["id"]
                record.direccion_ip = data["direccion_ip"]
                record.puerto_api = data["puerto_api"]
                record.usuario = data["usuario"]

                if record.id_API and record.direccion_ip and record.puerto_api and record.usuario:
                    record.valid = True
                else: raise ValidationError("Alguno de los campos esta faltando en la BD!")


        else:
            print("Oh no!")
            print(response.text)
            raise ValidationError("La respuesta de la API no ha sido valida")