# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class Departamentos(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "departamentos"
    _description = "Departamentos de Netcom Plus"
    _order = "name asc"

    # ---------------------------------------- Default Methods ------------------------------------


    
    # ---------------------------------------- Campos ---------------------------------
    name = fields.Char("Title", required=True)
    short = fields.Text("Descripcion corta",  required=True)
    description = fields.Text("Descripcion",  required=True)
    direccion = fields.Text("Direccion",  required=True)
    redirec = fields.Text("Enlace a redireccion")


    # ---------------------------------------- Metodos ---------------------------------
    @api.depends("redirec")
    def redireccion(self):
        url = "www.google.com"
        for offer in self:
            print("\n" + "-------------- \n")
            print(offer.redirec)
            url= offer.redirec
            print("\n" + "-------------- \n")

        if url.find("https") == -1:
            url = "https://" + url

        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new' 
        }
    
    @api.constrains('short')
    def _check_date_end(self):
        for record in self:
            if len(record.short) > 250:
                raise ValidationError("La este campo no debe tener mas de 250 caracteres")
            
    
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if len(record.name) < 3:
                raise ValidationError("El nombre debe tener mas de 3 caracteres\nPor favor trate de que el nombre sea descriptivo")
            
    @api.constrains('description')
    def _check_description(self):
        for record in self:
            if len(record.description) < 300:
                raise ValidationError("La descripcion debe tener al menos 300 caracteres.")

    @api.constrains('direccion')
    def _check_direction(self):
        for record in self:
            if len(record.direccion) < 50:
                raise ValidationError("La direccion debe tener al menos 50 caracteres.\n Puede incluir detalles que ayuden al trabajado a conocer la ubicacion como ciudad, municipio, parroquia etc..")