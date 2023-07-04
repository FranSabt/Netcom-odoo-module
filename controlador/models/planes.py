# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

class Planes(models.Model):
    _name = 'planes'
    _description = "Lista de planes de Netcom Plus"
    _order = "id desc"
    _sql_constraints = [
        ("check_precio", "CHECK(precio >= 0)", "El precio debe ser un numero positivo y major a cero."),
    ]

    #* Hay que colocar como name el nombre que uno desea que se refleje en la UI
    name = fields.Char("Nombre Comercial", required=True)
    nombre_lista = fields.Char("Nombre Lista", required=True)
    carga = fields.Char("Carga", required=True)
    descarga = fields.Char("Descarga", required=True)
    precio = fields.Float("Precio", required=True)
    activo = fields.Boolean("Activo el plan", default=True)
    id_API = fields.Integer("id")
    creado_en_api = fields.Boolean("Creado",default=False, readonly=True)
    # property_id = fields.Many2one("servicios", string="Property", required=True)


    @api.depends("name", "nombre_lista", "carga", "descarga", "precio")
    def enviar_a_api(self):
        # Obtener el registro actual
        registro_actual = self.ensure_one()
        # Construir los datos a enviar a la API

        
        datos = {
            'nombreComercial': registro_actual.name,
            'nombreLista': registro_actual.nombre_lista,
            'carga': registro_actual.carga,
            'descarga': registro_actual.descarga,
            'precio': registro_actual.precio,
        }
        
        for record in self:
            datos["nombreComercial"] = record.name
            datos["nombreLista"] = record.nombre_lista
            datos["carga"] = record.carga
            datos["descarga"] = record.descarga
            datos["precio"] = record.precio


        print("\n----------------")
        print(datos)
        print("----------------\n")

        # Enviar los datos a la API
        url = 'http://localhost:3333/plan/'
        response = requests.post(url, json=datos)

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
                if record.id_API:
                    record.creado_en_api = True


        else:
            print("Oh no!")
            print(response.text)
            raise ValidationError("Oh no!")
        