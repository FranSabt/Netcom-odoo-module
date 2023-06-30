# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class Netcom(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "netcom"
    _description = "Netcom Plus"
    _order = "id asc"
    _sql_constraints = [
        ("check_short", "CHECK(short > 205)", "La descripcion es de hasta 250 caracyeres"),
    ]
    
    # ---------------------------------------- Campos ---------------------------------
    name = fields.Char("Title", required=True)
    description = fields.Text("Descripcion",  required=True)
    short = fields.Text("Descripcion corta",  required=True)
    redirec = fields.Char("Enlace a redireccion")
    visible = fields.Boolean("Visible", default=True)


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

    # def button_name(self, arg):
    #     print("\n" + "-------------- \n")
    #     print(arg)
    #     print("\n" + "-------------- \n")
    #     url = self.redirec # Reemplaza esta URL por la que deseas utilizar
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': url,
    #         'target': 'new'
    #         }