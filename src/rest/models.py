# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Query(models.Model):
    name = models.CharField("Nombre", max_length=100, unique=True)
    sql = models.TextField("Raw SQL", help_text="Variables: %(nombre_de_variable)s")

    class Meta:
        verbose_name = "Query"
        verbose_name_plural = "Queries"

    def __str__(self):
        return self.name

    def get_params(self):
        return QueryParam.objects.filter(query=self).all()

    def joined_params(self):
        return [v for v in self.get_params()]
    joined_params.short_description = 'Parametros'

    def get_values(self):
        return QueryValue.objects.filter(query=self).all()

    def joined_values(self):
        return [v for v in self.get_values()]
    joined_values.short_description = 'Valores'


class QueryParam(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    param = models.TextField("Nombre de Parametro", max_length=15)

    class Meta:
        verbose_name = "Parametros (CSV)"
        verbose_name_plural = "Parametros (CSV)"

    def __str__(self):
        return self.param


class QueryValue(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    value = models.TextField("Nombre del Valor", max_length=15)

    class Meta:
        verbose_name = "Valor (CSV)"
        verbose_name_plural = "Valores (CSV)"

    def __str__(self):
        return self.value


class ModelJoin(models.Model):
    model = models.CharField("Nombre del Modelo", max_length=15)
    field = models.CharField("Campo del Modelo para el Parametro", max_length=15)
    name = models.CharField("Nombre", max_length=15)
    webservice = models.CharField("WebService de Destino (CSV)", max_length=15)
    param = models.CharField("Parametro en la Query", max_length=15)
    sql = models.TextField("SQL")
    syntax = models.CharField("Sintaxis de la respuesta (Aplica en CSV)", max_length=250, blank=True, default='')
    headers = models.CharField("Cabeceras de la respuesta (Aplica en CSV)", max_length=250, blank=True, default='')

    class Meta:
        verbose_name = "Adicion de Datos a Modelo (WS)"
        verbose_name_plural = "Adicion de Datos a Modelos (WS)"

    def __str__(self):
        return '%s - %s' % (self.model, self.name)

    def __unicode__(self):
        return '%s - %s' % (self.model, self.name)

    def ws_fields(self):
        fields = ModelJoinField.objects.filter(modeljoin=self).all()
        return [field.name for field in fields]


class ModelJoinField(models.Model):
    modeljoin = models.ForeignKey(ModelJoin)
    name = models.CharField("Nombre del Campo en el Modelo", max_length=15)

    class Meta:
        verbose_name = "Campo para Devolver"
        verbose_name_plural = "Campos para Devolver"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class ModelCustomFilter(models.Model):
    model = models.CharField("Nombre del Modelo", max_length=15)

    class Meta:
        verbose_name = "Filtro de Modelo Customizado"
        verbose_name_plural = "Filtros de Modelo Customizados"

    def __str__(self):
        return self.model

    def __unicode__(self):
        return self.model

    def fields(self):
        objects = ModelCustomFilterField.objects.filter(model=self)
        return {o.name: o.method for o in objects}


class ModelCustomFilterField(models.Model):
    model = models.ForeignKey(ModelCustomFilter)
    name = models.CharField("Nombre del Parametro", max_length=15)
    method = models.CharField("Metodo Customizado del Modelo", max_length=15)

    class Meta:
        verbose_name = "Campo"
        verbose_name_plural = "Campos"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
