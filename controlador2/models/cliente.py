# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

class Cliente(models.Model):
    _name = 'clientes'
    _description = "Lista de clientes de Netcom Plus"
    _order = "id desc"
    _sql_constraints = [
        ("constrain_name", "UNIQUE(name)", "El \"Cliente\" debe ser único."),
        ("constrain_client", "UNIQUE(client)", "El \"Cliente\" debe ser único."),
        ("constrain_onu", "UNIQUE(serial)", "El \"Serial de la ONU\"  debe ser único."),
    ]

    name = fields.Char("Username", readonly=True, compute="_compute_name")
    client = fields.Many2one("res.partner", string="Cliente", required=True)
    password= fields.Char("Serial de Onu", required=True) # serial = fields.Many2one("stock.lot", string="Serial")
    username = fields.Char("Username", required=True)
    fname = fields.Char("Nombre", required=True)   # Empresa
    lname = fields.Char("Apellido", required=True) # ID de cliente
    groupname = fields.Char("Plan", required=True)

    creationby = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user, readonly=True)
    updateby = fields.Many2one('res.users', string='Updated by', default=lambda self: self.env.user, readonly=True)

    @api.depends('client')
    def _compute_name(self):
        for record in self:
            if record.client:
                record.name = record.client.name
            else:
                record.name = ''

    @api.depends("name","password", "username", "fname", "lname", "groupname")
    def enviar_a_api(self):

        data = {}

        for record in self:
            data["name"] = record.name
            data["password"] = record.password
            data["username"] = record.username 
            data["fname"] = record.fname 
            data["lname"] = record.lname
            data["groupname"] = record.groupname
            
        print("\n----------------")
        print(data)
        print("----------------\n")

        # Enviar los datos a la API
        url = 'http://localhost:3003/'
        response = requests.post(url, data)

        # print(response)
        print("\n----------------", end="")
        print(response.status_code, end="")
        print("----------------\n")

        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            print(data) #! Dara error si no es un json
            # for record in self:
            #     record.id_API  = data["id"]
            #     record.nombre_lista = data["nombre_lista"]
            #     record.carga = data["carga"]
            #     record.descarga = data["descarga"]
            #     record.id_API = data["id"]
                

            #     if record.id_API and record.nombre_lista  and record.carga and record.descarga:
            #         record.activo = True
            #     else:
            #         raise ValidationError("Alguno de los campos esta faltando en la BD!")
        else:
            print("Oh no!")
            print(response.text)
            raise ValidationError("Oh no!")