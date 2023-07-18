# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
import ipaddress

"""
El modulo no crea los Planess en la API.
Sino que verifica su existencia en en BD de Router y rellena los campos si este existe.
Evitamos de este modo que un usuario malicioso pueda llenar la BD con datos innecesarios.
"""

class NAS(models.Model):
    _name = 'nas'
    _description = "Network Attached Storage"
    _order = "id desc"
    _sql_constraints = [
        ("name", "UNIQUE(name)", "El \"Nombre del NAS\" debe ser unico."),
    ]

    #* Hay que colocar como name el nombre que uno desea que se refleje en la UI
    name       = fields.Char("Nombre del NAS", required=True)
    ip_address = fields.Char(string="Dirección IP", required=True)
    secret     = fields.Char("Secret", required=True)
    id_rad     = fields.Char("ID de Radius", readonly=True)
    activo     = fields.Boolean(default=False, readonly=True)


    creationby   = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user, readonly=True)
    updateby     = fields.Many2one('res.users', string='Updated by', default=lambda self: self.env.user, readonly=True)

    @api.constrains('ip_address')
    def _check_ip_address(self):
        for record in self:
            try:
                ipaddress.ip_address(record.ip_address)
            except ValueError:
                raise models.ValidationError("La dirección IP no es válida.")


    @api.depends("name", "nombre_lista", "carga", "descarga", "precio")
    def enviar_a_api(self):

        name = ""
        for record in self:
            name = record.name

        """
        data = {}
        for record in self:
            data["name"] = record.name
            data["ip_address"] = record.ip_address
            data["secret"] = record.secret
            data["id_rad"] = record.id_rad
            data["activo"] = record.activo

        """

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