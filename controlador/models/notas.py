from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Notas(models.Model):
    _name = 'notas'
    
    servicio_id = fields.Many2one("servicios", string="Servicio")
    notas = fields.Text("Notas")