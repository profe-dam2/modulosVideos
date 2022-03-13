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

    def name_get(self):
        listaDptos = []
        for dpto in self:
            listaDptos.append(dpto.id, dpto.nombreDpto)
        return listaDptos

class empleado(models.Model):
    _name = 'proyectos.empleado'
    _description = 'Define los atributos de un empleado'

    # Atributos
    dniEmpleado = fields.Char(string='DNI', required=True)
    nombreEmpleado = fields.Char(string='Nombre y apellidos', required=True)
    fechaNacimiento = fields.Date(string='Fecha Nacimiento', required=True, default = fields.date.today())
    direccionEmpleado = fields.Char(string='Direccon')
    telefonoEmpleado = fields.Char(string='Telefono')
    edad = fields.Integer('Edad', compute='_getEdad')

    #Relacion de tablas
    departamento_id = fields.Many2one('proyectos.departamento', string='Departamento')
    proyecto_ids = fields.Many2many('proyectos.proyecto', string='Proyectos')


    @api.depends('fechaNacimiento')
    def _getEdad(self):
        hoy = date.today()
        for empleado in self:
            empleado.edad = relativedelta(hoy, empleado.fechaNacimiento).years

    @api.constrains('fechaNacimiento')
    def _checkEdad(self):
        for empleado in self:
            if (empleado.edad < 18):
                raise exceptions.ValidationError("El empleado no puede ser menor de edad")
    
    @api.constrains('dniEmpleado')
    def _checkDNI(self):
        for empleado in self:
            if (len(empleado.dniEmpleado) > 9):
                raise exceptions.ValidationError("El DNI no puede tener mas 9 caracteres")
            if (len(empleado.dniEmpleado) < 9):
                raise exceptions.ValidationError("El DNI no puede tener menos 9 caracteres")

class proyecto(models.Model):
     _name = 'proyectos.proyecto'
     _description = 'Define los atributos de un proyecto'

     #Atributos
     nombreProyecto = fields.Char(string='Nombre proyecto', required=True)
     tipoProyecto = fields.Selection(string='Tipo de poryecto', selection=[('f','Front-End'),('b','Back-End')], help='Tipo de proyecto al que se esta destinando' )
     descripcionProyecto = fields.Text(string='Descripcion del proyecto')
     fechaInicio = fields.Date(string='Fecha de Inicio', required=True)
     fechaFin = fields.Date(string='Fecha de fin', required=True)
     #dias = fields.Integer(string='Dias')
     #Relacion entre tablas
     empleado_id = fields.Many2many('proyectos.empleado', string='Empleados')

     @api.constrains('fechaFin')
     def _checkFechaFin(self):
         for proyecto in self:
             if relativedelta(proyecto.fechaInicio, proyecto.fechaFin).days > 0:
                 raise exceptions.ValidationError("La fecha de fin no puede ser inferior a la fecha de inicio")
     
     @api.constrains('fechaInicio')
     def _checkFechaInicio(self):
         hoy = date.today()
         for proyecto in self:
             diasCalculados = relativedelta(hoy, proyecto.fechaInicio).days
             if ( diasCalculados > 0):
                 raise exceptions.ValidationError("La fecha no puede ser anterior a la fecha actual")

     

