# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

"""
El modulocrea un Sevicio en la API.
"""

"""#TODO Crear boton de actualizacion de datos automatica
    Crear boton Para actualizar estado del servicio.
""" 
class Servicios(models.Model):
    _name = 'servicios'
    _description = "Lista de Servicios de Netcom Plus"
    _order = "id desc"
    _sql_constraints = [
        ("nombre_cliente", "UNIQUE(nombre_cliente)", "El \"Nombre del Cliente\" debe ser unico."),
    ]
    
    
    id_API = fields.Integer("id")
    hostname = fields.Char("Hostname", default="no hostname", readonly=True)
    name = fields.Char("Nombre del Cliente")
    direccion_ip = fields.Char("Direccion IPV4")
    estado_cliente = fields.Selection(
        selection=[
            ("1", "Activo"),
            ("2", "Suspendido"),
            ("3", "Cancelado"),
        ],
        string="Estado del Cliente",
        default=1
        )
    creado_en_api = fields.Boolean("Creado",default=False, readonly=True)
    actualizado = fields.Boolean("actualizado el plan", readonly=True)

    #* RELACIONES *#
    plan_id = fields.Many2one('planes', string='Plan')
    router_id = fields.Many2one("routers", string="Router")
    # notas = fields.One2many("notas", "servicio_id", string="Notas")

    
    @api.depends("id_API", "hostane", "direccion_ip", "plan_id", "router_id", "estado_cliente")
    def enviar_a_api(self):

        datos = {}
        
        for record in self:
            datos["hostname"] = record.hostname
            datos["direccionIp"] = record.direccion_ip
            datos["planId"] = record.plan_id.id_API
            datos["routerId"] = record.router_id.id_API
            datos["estado_id"] = int(record.estado_cliente)
            datos["nombreCliente"] = record.name

        print("\n----------------")
        print(datos)
        print("----------------\n")

        # Enviar los datos a la API
        url = 'http://localhost:3333/servicio/'
        response = None


        for record in self:
            if record.creado_en_api:
                response = requests.put(url, json=datos)
            else:
                response = requests.post(url, json=datos)
                #! Esta ruta no existe copn PUT en la API de NEST, hay que crearla!

        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            print(data)
            for record in self:
                record.hostname = data["hostname"]
                record.id_API  = data["id"]
                if record.hostname and record.id_API:
                    record.actualizado = True
                    record.creado_en_api = True
                else: raise ValidationError("Hubo un error al recibir los datos!")


        else:
            print("Oh no!")
            print(response.text)
            raise ValidationError("La respuesta de la API no ha sido valida")
        
    @api.onchange('name', 'plan', 'router', 'direccion_ip', 'estado_cliente')
    def _onchange_name(self):
        self.actualizado = False