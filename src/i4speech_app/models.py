# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.db.models import Avg

import legibilidad


# Copie y pegue los modelos del archivo models.py SACANDO los que eran por defecto de django
# Le di formato e indentaciones adecuados
# Le agregue @staticmethod al metodo prom_cr del modelo Cr

class Autores(models.Model):
    nombre = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    twitter = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nombre


class Cr(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    @staticmethod
    def prom_cr(idautor):
        prom = Cr.objects.filter(idtexto__idautor_id=idautor).aggregate(prom_cr=Avg('resultado'))
        return prom.get('prom_cr')


class Escalafh(models.Model):
    inf = models.IntegerField(
        blank=True,
        null=True
    )
    sup = models.IntegerField(
        blank=True,
        null=True
    )
    resultado = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


class Escalain(models.Model):
    inf = models.IntegerField(blank=True, null=True)
    sup = models.IntegerField(blank=True, null=True)
    resultado = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


class Escalagu(models.Model):
    inf = models.FloatField(
        blank=True,
        null=True
    )
    sup = models.FloatField(
        blank=True,
        null=True
    )
    resultado = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


class Escalasp(models.Model):
    inf = models.IntegerField(
        blank=True,
        null=True
    )
    sup = models.IntegerField(
        blank=True,
        null=True
    )
    resultado = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    tipopublicacion = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    estudios = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


class Escalamu(models.Model):
    inf = models.IntegerField(
        blank=True,
        null=True
    )
    sup = models.IntegerField(
        blank=True,
        null=True
    )
    resultado = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )


class Fh(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    def prom_fh(idautor):
        prom = Fh.objects.filter(idtexto__idautor_id=idautor).aggregate(prom_fh=Avg('resultado'))
        return prom.get('prom_fh')


class Gu(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    def prom_gu(idautor):
        prom = Gu.objects.filter(idtexto__idautor_id=idautor).aggregate(prom_gu=Avg('resultado'))
        return prom.get('prom_gu')


class Mu(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    def prom_mu(idautor):
        prom = Mu.objects.filter(idtexto__idautor_id=idautor).aggregate(prom_mu=Avg('resultado'))
        return prom.get('prom_mu')


class Sp(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    def prom_sp(idautor):
        prom = Sp.objects.filter(idtexto__idautor_id=idautor).aggregate(prom_sp=Avg('resultado'))
        return prom.get('prom_sp')


class Ocasiones(models.Model):
    ocasion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.ocasion


class Textos(models.Model):
    texto = models.TextField()
    idautor = models.ForeignKey(
        'Autores',
        models.DO_NOTHING,
        db_column='idautor'
    )
    fecha = models.DateField(
        blank=True,
        null=True
    )
    titulo = models.CharField(max_length=255)
    idocasion = models.ForeignKey(
        'Ocasiones',
        models.DO_NOTHING,
        db_column='idocasion'
    )

    def __str__(self):
        return self.texto

    def save(self, *args, **kwargs):
        super(Textos, self).save(*args, **kwargs)  # Call the "real" save() method.
        cr = Cr.objects.create(
            idtexto=self,
            resultado=legibilidad.crawford(self.texto)
        )
        cr.save()

        mu = Mu.objects.create(
            idtexto=self,
            resultado=legibilidad.mu(self.texto)
        )
        mu.save()

        fh = Fh.objects.create(
            idtexto=self,
            resultado=legibilidad.fernandez_huerta(self.texto)
        )
        fh.save()

        sp = Sp.objects.create(
            idtexto=self,
            resultado=legibilidad.szigriszt_pazos(self.texto)
        )
        sp.save()

        gu = Gu.objects.create(
            idtexto=self,
            resultado=legibilidad.gutierrez(self.texto)
        )
        gu.save()

    def get_absolute_url(self):
        return reverse(
            'textodetalle',
            kwargs={'pk': self.id}
        )
