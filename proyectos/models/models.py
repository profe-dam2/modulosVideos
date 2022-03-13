# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class proyectos(models.Model):
#     _name = 'proyectos.proyectos'
#     _description = 'proyectos.proyectos'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


from odoo import models, fields, api, exceptions
from dateutil.relativedelta import *
from datetime import date

class departamento(models.Model):
    _name = 'proyectos.departamento'
    _description = 'Define los atributos de un departamento'

    # Atributos
    nombreDpto = fields.Char(string='Nombre departamento', required=True)

    #Relacion entre tablas
    empleado_id = fields.One2many('proyectos.empleado','departamento_id', string='Departamento')

class empleado(models.Model):
    _name = 'proyectos.empleado'
    _description = 'Define los atributos de un empleado'

    # Atributos
    dniEmpleado = fields.Char(string='DNI', required=True)
    nombreEmpleado = fields.Char(string='Nombre y apellidos', required=True)
    fechaNacimiento = fields.Date(string='Fecha Nacimiento', required=True, default = fields.date.today())
    direccionEmpleado = fields.Char(string='Direccon')
    telefonoEmpleado = fields.Char(string='Telefono')

    #Relacion de tablas
    departamento_id = fields.Many2one('proyectos.departamento', string='Empleados')
    proyecto_ids = fields.Many2many('proyectos.proyecto', string='Proyectos')


class proyecto(models.Model):
     _name = 'proyectos.proyecto'
     _description = 'Define los atributos de un proyecto'

     #Atributos
     nombreProyecto = fields.Char(string='Nombre proyecto', required=True)
     tipoProyecto = fields.Selection(string='Tipo de poryecto', selection=[('f','Front-End'),('b','Back-End')], help='Tipo de proyecto al que se esta destinando' )
     descripcionProyecto = fields.Text(string='Descripcion del proyecto')
     fechaInicio = fields.Date(string='Fecha de Inicio', required=True)
     fechaFin = fields.Date(string='Fecha de fin', required=True)
     dias = fields.Integer(string="dias")
     #Relacion entre tablas
     empleado_id = fields.Many2many('proyectos.empleado', string='Empleados')

     @api.constrains('fechaInicio')
     def _checkFechaInicio(self):
         hoy = date.today()
         for proyecto in self:
             proyecto.dias = relativedelta(hoy, proyecto.fechaInicio).days
             if (proyecto.dias > 0):
                 raise exceptions.ValidationError("La fecha no puede ser anterior a la fecha actual")

