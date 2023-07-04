# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

class Servicios(models.Model):
    _name = 'servicios'
    
    id_API = fields.Integer("id")
    hostname = fields.Char("Hostname", default="no hostname", readonly=True)
    nombre_cliente = fields.Char("Nombre del Cliente")
    direccion_ip = fields.Char("Dire IPV4")
    plan_id = fields.Many2one('planes', string='Plan')
    router_id = fields.Integer("Id del router conectado")
    estado_cliente = fields.Integer("Estado del cliente")
    creado_en_api = fields.Boolean("Creado",default=False, readonly=True)

    #! Crear un campo condicional para no enviar 2 veces la data
    #! Campo que diga que todos los datos se crearon correctamente
    
    @api.depends("id_API", "hostane", "direccion_ip", "plan_id", "router_id", "estado_cliente")
    def enviar_a_api(self):
        # Obtener el registro actual
        registro_actual = self.ensure_one()
        # Construir los datos a enviar a la API

        
        datos = {
            'id_API': registro_actual.id_API,
            'hostname': registro_actual.hostname,
            'nombre_cliente': registro_actual.nombre_cliente,
            'direccion_ip': registro_actual.direccion_ip,
            'plan_id': registro_actual.plan_id,
            'router_id': registro_actual.router_id,
            'estado_cliente': registro_actual.estado_cliente,
        }
        
        for record in self:
            datos["hostname"] = record.hostname
            datos["direccionIp"] = record.direccion_ip
            datos["planId"] = record.plan_id
            datos["routerId"] = record.router_id
            datos["estado_cliente"] = record.router_id
            datos["nombreCliente"] = record.nombre_cliente

        print("\n----------------")
        print(datos)
        print("----------------\n")

        # Enviar los datos a la API
        url = 'http://localhost:3333/servicio/'
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
                record.hostname = data["hostname"]
                record.id_API  = data["id"]
                if record.hostname and record.id_API:
                    record.creado_en_api = True


        else:
            print("Oh no!")
            print(response.text)
            raise ValidationError("Oh no!")
        


        
        
        # Manejar la respuesta de la API
        # if response.status_code == 200:
        #     # La API aceptó los datos
        #     self.env.user.notify_warning('Los datos se enviaron correctamente a la API')
        # else:
        #     # La API rechazó los datos
        #     self.env.user.notify_warning('No se pudieron enviar los datos a la API. Código de error: %s' % response.status_code)
    
    # @api.model
    # def create(self, vals):
    #     record = super(Servicios, self).create(vals)
    #     record._init()
    #     return record
    
    # def get_data(self):
    #     url = 'http://localhost:3333/servicio/'
    #     response = requests.post(url, json={
    #         "hostname": "FranSab",
    #         "nombreCliente": "franSab",
    #         "direccionIp": "182.141.33.55",
    #         "planId": "1",
    #         "routerId": "1"
    #     })
    #     return response.json()

    # def _init(self):
    #     data = self.get_data()
    #     for d in data:
    #         self.env['api.data'].create({
    #             'name': d['hostname'],
    #             'hostname': d['hostname'],
    #             'nombre_cliente': d['nombreCliente'],
    #             'direccion_ip': d['direccionIp'], 
    #             'plan_id': d['planId'],
    #             'router_id': d['routerId']
    #         })