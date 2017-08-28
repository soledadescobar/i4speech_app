# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Tweet(models.Model):
    term = models.CharField(
        "Término",
        max_length=100,
        blank=True,
        null=True,
        default=None,
        help_text="Término de Búsqueda. Ejemplos: @Usuario ó #Hashtag ó Expresión. Solo admite 1 término."
    )
    raw_query = models.CharField(
        "Twitter Query",
        max_length=250,
        blank=True,
        null=True,
        default=None,
        help_text="Query de Búsqueda Twitter. Realizar una búsqueda en Twitter y Copiar la url luego de ?s=."
                  "Experimental"
    )
    since = models.DateField("Desde Fecha", null=True, blank=True, default=None)
    until = models.DateField("Hasta Fecha", null=True, blank=True, default=None)
    since_id = models.BigIntegerField("Desde ID", blank=True, null=True, default=None)
    max_id = models.BigIntegerField("Hasta ID", blank=True, null=True, default=None)
    created_at = models.DateTimeField("Fecha", auto_now_add=True)
    max_results = models.IntegerField(
        "Cantidad",
        default=1000,
        blank=True,
        help_text="Cantidad Minima Esperada de Resultados a Cargar. Por defecto espera al menos 1.000 Resultados."
    )

    class Meta:
        verbose_name = "Búsqueda de Tweet"
        verbose_name_plural = "Búsqueda de Tweets"

    def __str__(self):
        return self.term if self.term else self.raw_query

    def results_count(self):
        return TweetResult.objects.filter(tweet=self).count()
    results_count.short_description = "Resultados Obtenidos"


class TweetResult(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    result_id = models.BigIntegerField("ID Tweet")
    screen_name = models.CharField("Screen Name", max_length=100)

    class Meta:
        verbose_name = "Tweet Obtenido"
        verbose_name_plural = "Tweets Obtenidos"

    def __str__(self):
        return "@%s #%d" % (self.screen_name, self.result_id)


class Timeline(models.Model):
    user_id = models.BigIntegerField("ID de Usuario", blank=True, default=0)
    screen_name = models.CharField("Screen Name", max_length=100, blank=True, default="")
    since_id = models.BigIntegerField("Desde ID", blank=True, default=0)
    max_id = models.BigIntegerField("Hasta ID", blank=True, default=0)
    created_at = models.DateTimeField("Fecha", auto_now_add=True)
    results_count = models.IntegerField(blank=True, null=True, default=None)

    class Meta:
        verbose_name = "Búsqueda de Tweet"
        verbose_name_plural = "Búsqueda de Tweets"

    def __str__(self):
        return self.screen_name if self.screen_name else self.user_id