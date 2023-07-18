# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests
from requests.exceptions import ConnectionError

class Cliente(models.Model):
    _name = 'clientes'
    _description = "Lista de clientes de Netcom Plus"
    _order = "id desc"
    _sql_constraints = [
        ("constrain_name", "UNIQUE(name)", "El \"Cliente\" debe ser único."),
        ("constrain_client", "UNIQUE(client)", "El \"Cliente\" debe ser único."),
        ("constrain_onu", "UNIQUE(serial)", "El \"Serial de la ONU\"  debe ser único."),
    ]

    name      = fields.Char("Username", readonly=True, compute="_compute_name")
    client    = fields.Many2one("res.partner", string="Cliente", required=True)
    # password  = fields.Char("Serial de Onu", required=True) 
    # password = fields.Many2one("stock.lot", string="Serial")
    username  = fields.Char("Serial de Onu", required=True) 
    fname     = fields.Selection(
        selection=[
            ('Cod-Netcom', 'Netcom'),
            ('Cod-NC', 'NC'),
        ],
        string="Empresa",
        required=True
        )
    lname     = fields.Char("Wisphub ID", required=True) # ID de cliente en Wisphub
    groupname = fields.Many2one("plan", string="Plan", required=True)

    creationby = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user, readonly=True)
    updateby   = fields.Many2one('res.users', string='Updated by', default=lambda self: self.env.user, readonly=True)

    @api.depends('client')
    def _compute_name(self):
        for record in self:
            if record.client:
                record.name = record.client.name
            else:
                record.name = ''

    @api.depends("name", "username", "fname", "lname", "groupname")
    def enviar_a_api(self):
        data = {}

        for record in self:
            data["name"] = record.name
            data["username"] = record.username 
            data["fname"] = record.fname 
            data["lname"] = record.lname
            data["groupname"] = record.groupname.groupname

        print("\n----------------")
        print(data)
        print("----------------\n")

        # Enviar los datos a la API
        url = 'http://localhost:3003/'

        try:
            response = requests.post(url, data)
            response.raise_for_status()  # Esto lanzará una excepción para códigos de estado HTTP >= 400
            if response.status_code == 200 or response.status_code == 201:
                print("\n----------------", end="")
                print(response.status_code, end="")
                print("----------------\n")

                data = response.json()
                print(data)
                # Resto de tu lógica con la respuesta exitosa

                # for record in self:
                #     record.id_API  = data["id"]
                #     record.nombre_lista = data["nombre_lista"]
                #     record.carga = data["carga"]
                #     record.descarga = data["descarga"]
                #     record.id_API = data["id"]
                #
                #     if record.id_API and record.nombre_lista  and record.carga and record.descarga:
                #         record.activo = True
                #     else:
                #         raise ValidationError("Alguno de los campos esta faltando en la BD!")

            else:
                print("Oh no!")
                print(response.text)
                raise ValidationError("Oh no! Hubo un error en la API.")

        except ConnectionError as e:
            print("Error de conexión:", e)
            raise ValidationError("No se pudo establecer la conexión con la API.")
        except requests.exceptions.RequestException as e:
            print("Error en la solicitud:", e)
            raise ValidationError("Hubo un error en la solicitud a la API.")