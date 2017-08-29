# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Frente(models.Model):
    name = models.CharField("Frente", max_length=120)
    color = models.CharField("Color Hexadecimal sin #", max_length=6)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values():
        return ['id', 'name']


class Bloque(models.Model):
    name = models.CharField("Bloque", max_length=120)
    frente = models.OneToOneField(Frente, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values():
        return ['id', 'name']


class Provincia(models.Model):
    name = models.CharField("Provincia", max_length=120)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values():
        return ['id', 'name']


class Posicion(models.Model):
    name = models.CharField(
        "Posición",
        max_length=120,
        help_text="Posición o Cargo a Ocupar"
    )

    class Meta:
        verbose_name = "Posición"
        verbose_name_plural = "Posiciones"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Candidato(models.Model):
    name = models.CharField(
        "Nombre",
        max_length=120
    )
    screen_name = models.CharField(
        "Screen Name",
        max_length=120,
        help_text="Usuario de Twitter",
        unique=True
    )
    user_id = models.BigIntegerField(
        "Twitter User ID",
        null=True,
        blank=True,
        default=None,
        help_text="ID de usuario de Twitter (Se obtiene de forma automatica al guardar)",
        editable=False
    )
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    bloque = models.ForeignKey(
        Bloque,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    frente = models.ForeignKey(
        Frente,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values(extra=True):
        respone = ['id', 'name', 'screen_name']
        if extra:
            respone.extend(['user_id', 'frente__name', 'bloque__name'])
        return respone


class Lista(models.Model):
    name = models.CharField("Nombre", max_length=120)
    frente = models.ForeignKey(Frente, on_delete=models.CASCADE)
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    posicion = models.ForeignKey(
        Posicion,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(
        "Keyword",
        max_length=100,
        help_text="Keyword o Hashtag comenzando con #"
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
