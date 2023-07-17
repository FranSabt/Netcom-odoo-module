# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
import re

class Zona(models.Model):
    _name = 'zona'
    _description = "Zona de NAS"
    _order = "id desc"
    _sql_constraints = [
        ("name", "UNIQUE(name)", "El \"Nombre del NAS\" debe ser unico."),
    ]

    coordenadas_regex = r'^-?\d+(?:\.\d+)?, -?\d+(?:\.\d+)?$'
    coordenadas_validas = "Las coordenadas deben tener el formato 'x, y'."

    #* Hay que colocar como name el nombre que uno desea que se refleje en la UI
    name = fields.Char("Nombre del NAS", required=True)
    coord = fields.Char(string="Coordenadas", required=True, 
                        help="Coordenadas en formato 'x, y'.")
    tlf = fields.Char("Tlf:")
    codigo_zona = fields.Char("Código de Zona")
    Nas = fields.Many2one("nas", string="NAS")
    activo = fields.Boolean(default=False)


    creationdate =   fields.Char("Creado: ", readonly=True)
    updatedate = fields.Char("Actualizado: ", readonly=True)
    creationby = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user, readonly=True)
    updateby = fields.Many2one('res.users', string='Updated by', default=lambda self: self.env.user, readonly=True)


    @api.constrains('coord')
    def _check_coordenadas(self):
        for record in self:
            if record.coord and not re.match(self.coordenadas_regex, record.coord):
                raise models.ValidationError(self.coordenadas_validas)

    @api.depends("name", "nombre_lista", "carga", "descarga", "precio")
    def enviar_a_api_zona(self):

        name = ""
        for record in self:
            name = record.name

        # Enviar los datos a la API
        url = 'http://localhost:3333/plan/name/' + name
        response = requests.get(url)

        # print(response)
        print("\n----------------", end="")
        print(response.status_code, end="")
        print("----------------\n")

        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            print(data)
            for record in self:
                record.id_API  = data["id"]
                record.nombre_lista = data["nombre_lista"]
                record.carga = data["carga"]
                record.descarga = data["descarga"]
                record.id_API = data["id"]
                

                if record.id_API and record.nombre_lista  and record.carga and record.descarga:
                    record.activo = True
                else:
                    raise ValidationError("Alguno de los campos esta faltando en la BD!")
        else:
            print("Oh no!")
            print(response.text)
            raise ValidationError("Oh no!")