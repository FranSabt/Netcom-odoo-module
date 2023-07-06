# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

class Routers(models.Model):
    _name = 'routers'
    _description = "Lista de routers de Netcom Plus"
    _order = "id desc"
    _sql_constraints = [
        ("check_precio", "CHECK(precio >= 0)", "El precio debe ser un numero positivo y major a cero."),
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
        # Obtener el registro actual
        # registro_actual = self.ensure_one()
        # Construir los datos a enviar a la API


        name = ""
        for record in self:
            name = record.name
            print(record.name)



        print("\n----------------")
        print(name)
        print("----------------\n")

        # Enviar los datos a la API
        url = 'http://localhost:3333/router/name/' + name
        response = requests.get(url)
        # print(response)
        print("\n----------------")
        print(response.status_code)
        print(type(response.status_code))
        print("----------------\n")

        if response.status_code == 200 or response.status_code == 201:
            print("\n----------------")
            print("Exclesior")
            data = response.json()
            print(data)
            for record in self:
                record.id_API  = data["id"]
                record.direccion_ip = data["direccion_ip"]
                record.puerto_api = data["puerto_api"]
                record.usuario = data["usuario"]

                if record.id_API:
                    record.valid = True


        else:
            print("Oh no!")
            print(response.text)
            raise ValidationError("Oh no!")
        