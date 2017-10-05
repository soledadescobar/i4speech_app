# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ProvinciaManager(models.Manager):
    def get_by_bloques(self, bloques, **kwargs):
        objs = Bloque.objects.filter(id__in=bloques)
        ids = [o.provincia_id for o in objs]
        return super(ProvinciaManager, self).filter(id__in=ids)


class Provincia(models.Model):
    objects = ProvinciaManager()
    name = models.CharField("Provincia", max_length=120)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values():
        return ['id', 'name']

    def get_bloques(self):
        objects = Bloque.objects.filter(provincia=self)


class Distrito(models.Model):
    name = models.CharField("Distrito", max_length=120)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values():
        return ['id', 'name']


class Frente(models.Model):
    name = models.CharField("Frente", max_length=120)
    color = models.CharField("Color Hexadecimal sin #", max_length=6)
    rest_visible = models.BooleanField(
        "REST",
        blank=True,
        default=False,
        help_text="Activa si este objecto puede ser visualizado en un WebService via REST"
    )

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values():
        return ['id', 'name']


class Bloque(models.Model):
    name = models.CharField("Bloque", max_length=120)
    frente = models.ForeignKey(Frente, on_delete=models.CASCADE)
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None
    )
    rest_visible = models.BooleanField(
        "REST",
        blank=True,
        default=False,
        help_text="Activa si este objecto puede ser visualizado en un WebService via REST"
    )

    class Meta:
        verbose_name = 'Partido/Alianza'
        verbose_name_plural = 'Partidos/Alianzas'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values():
        return ['id', 'name']


class Posicion(models.Model):
    name = models.CharField(
        "Categoría",
        max_length=120,
        help_text="Categoría/Posición/Cargo a Ocupar"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @staticmethod
    def ws_values():
        response = ['id', 'name']

        return response


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
        help_text="ID de usuario de Twitter (Se obtiene de forma automática al guardar)",
        editable=False
    )
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        blank=True,
        default=-1
    )
    distrito = models.ForeignKey(
        Distrito,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    posicion = models.ForeignKey(
        Posicion,
        on_delete=models.CASCADE,
        blank=True,
        default=-1
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
    rest_visible = models.BooleanField(
        "REST",
        blank=True,
        default=False,
        help_text="Activa si este objecto puede ser visualizado en un WebService via REST"
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
    name = models.CharField("Nombre", max_length=250)
    number = models.IntegerField("Número")
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)

    rest_visible = models.BooleanField(
        "REST",
        blank=True,
        default=False,
        help_text="Activa si este objecto puede ser visualizado en un WebService via REST"
    )

    class Meta:
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class ListaSeccion(models.Model):

    PRESIDENTE = 'PN'
    DIPUTADOS_NACIONALES = 'DN'
    DIPUTADOS_PROVINCIALES = 'DP'
    DIPUTADOS_LEGISLATURA = 'DL'
    SENADORES_NACIONALES = 'SN'
    LEGISLADORES = 'LG'
    PARLAMENTARIOS = 'PM'
    GOBERNADOR = 'GB'

    TYPES = (
        (PRESIDENTE, 'Presidente y Vice Presidente'),
        (DIPUTADOS_NACIONALES, 'Diputados Nacionales'),
        (DIPUTADOS_PROVINCIALES, 'Diputados Provinciales'),
        (DIPUTADOS_LEGISLATURA, 'Diputados Legislatura'),
        (SENADORES_NACIONALES, 'Senadores Nacionales'),
        (LEGISLADORES, 'Legisladores'),
        (PARLAMENTARIOS, 'Parlamentarios'),
        (GOBERNADOR, 'Gobernador')
    )

    lista = models.ForeignKey(Lista, on_delete=models.CASCADE)

    tipo = models.CharField(
        max_length=2,
        choices=TYPES
    )

    def __unicode__(self):
        return "%s - %s" % (self.lista, self.tipo)

    class Meta:
        verbose_name = 'Seccion'
        verbose_name_plural = 'Secciones'


class ListaSeccionCandidato(models.Model):

    TITULAR = 'TI'
    SUPLENTE = 'SU'

    TYPES = (
        (TITULAR, 'Titular'),
        (SUPLENTE, 'Suplente')
    )

    lista_seccion = models.ForeignKey(ListaSeccion, on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=2,
        choices=TYPES
    )
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    orden = models.IntegerField("Posición")

    class Meta:
        verbose_name = 'Candidato'
        verbose_name_plural = 'Candidatos'


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
