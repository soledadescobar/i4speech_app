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

    class Meta:
        managed = False
        db_table = 'autores'

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

    class Meta:
        managed = False
        db_table = 'cr'

    @staticmethod
    def prom_cr():
        prom = Cr.objects.values(
            'idtexto__idautor__nombre'
        ).annotate(
            prom_cr=Avg('resultado')
        ).order_by(
            'idtexto__idautor__nombre'
        )
        return prom


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

    class Meta:
        managed = False
        db_table = 'escalafh'


class Escalain(models.Model):
    inf = models.IntegerField(blank=True, null=True)
    sup = models.IntegerField(blank=True, null=True)
    resultado = models.CharField(
        max_length=50,
        blank=True,
        null=True)

    class Meta:
        managed = False
        db_table = 'escalain'


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

    class Meta:
        managed = False
        db_table = 'escalagu'


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

    class Meta:
        managed = False
        db_table = 'escalasp'


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

    class Meta:
        managed = False
        db_table = 'escalamu'


class Fh(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    class Meta:
        managed = False
        db_table = 'fh'


class Gu(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    class Meta:
        managed = False
        db_table = 'gu'


class Mu(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    class Meta:
        managed = False
        db_table = 'mu'


class Sp(models.Model):
    idtexto = models.OneToOneField(
        'Textos',
        models.DO_NOTHING,
        db_column='idtexto',
        primary_key=True,
        unique=True
    )
    resultado = models.FloatField()

    class Meta:
        managed = False
        db_table = 'sp'


class Ocasiones(models.Model):
    ocasion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ocasiones'

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


    class Meta:
        managed = False
        db_table = 'textos'

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

