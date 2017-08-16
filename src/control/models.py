# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Frente(models.Model):
    name = models.CharField("Frente", max_length=120)

    def __str__(self):
        return self.name


class Bloque(models.Model):
    name = models.CharField("Bloque", max_length=120)
    frente = models.ForeignKey(Frente, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Provincia(models.Model):
    name = models.CharField("Provincia", max_length=120)

    def __str__(self):
        return self.name

class Posicion(models.Model):
    name = models.CharField("Posición", max_length=120)

    class Meta:
        verbose_name = "Posición"
        verbose_name_plural = "Posiciones"

    def __str__(self):
        return self.name


class Candidato(models.Model):
    name = models.CharField("Nombre", max_length=120)
    screen_name = models.CharField("Screen Name", max_length=120)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    frente = models.ForeignKey(Frente, on_delete=models.CASCADE)
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lista(models.Model):
    name = models.CharField("Nombre", max_length=120)
    frente = models.ForeignKey(Frente, on_delete=models.CASCADE)
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField("Keyword", max_length=100, help_text="Keyword o Hashtag comenzando con #")

    def __str__(self):
        return self.name
