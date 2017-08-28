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
    name = models.CharField("Nombre", max_length=15)
    sql = models.TextField("SQL")

    class Meta:
        verbose_name = "Adicion de Datos a Modelo (WS)"
        verbose_name_plural = "Adicion de Datos a Modelos (WS)"

    def __str__(self):
        return '%s - %s' % (self.model, self.name)

    @property
    def ws_fields(self):
        fields = ModelJoinField.objects.filter(modeljoin=self).order_by('order')
        result = {}
        for field in fields:
            result[field.name] = field.field
        return result


class ModelJoinField(models.Model):
    modeljoin = models.ForeignKey(ModelJoin, on_delete=models.CASCADE)
    field = models.CharField("Campo del Modelo", max_length=15)
    name = models.CharField("Parametro en la Query", max_length=15)
    order = models.IntegerField("Orden")

    class Meta:
        verbose_name = "Campo del Modelo"
        verbose_name_plural = "Campos del Modelo"

    def __str__(self):
        return self.field