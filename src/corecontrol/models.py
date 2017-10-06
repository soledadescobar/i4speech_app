# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from control.models import Candidato, Keyword


# Create your models here.
class KnownUsers(models.Model):
    user_id = models.BigIntegerField(unique=True)
    screen_name = models.CharField(max_length=100)

    def __getitem__(self, key):
        return getattr(self, key)


class ApiKey(models.Model):
    name = models.CharField(
        "Nombre",
        max_length=10,
        help_text="Nombre corto para representar las keys."
                  "Máximo 10 caracateres. Ejemplo: pst-gs1 para una key cargada por Gabriel Scarcella de PST"
    )
    consumer_key = models.CharField(max_length=100)
    consumer_secret = models.CharField(max_length=100)
    api_key = models.CharField("access_token", max_length=100)
    api_secret = models.CharField("access_token_secret", max_length=100)

    def __str__(self):
        return self.name


class ServerType(models.Model):
    name = models.CharField("Nombre", max_length=50)

    class Meta:
        verbose_name = "Tipo de Servidor"
        verbose_name_plural = "Tipos de Servidor"

    def __str__(self):
        return self.name


class Server(models.Model):
    server_type = models.ForeignKey(ServerType, on_delete=models.CASCADE)
    name = models.CharField("Nombre", max_length=100)
    ip = models.GenericIPAddressField()
    apikey = models.ForeignKey(
        ApiKey,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"

    def __str__(self):
        return self.name

    def get_apikeys(self):
        return {
            'consumer_key': self.apikey.consumer_key,
            'consumer_secret': self.apikey.consumer_secret,
            'access_token': self.apikey.api_key,
            'access_token_secret': self.apikey.api_secret
        }

    def usage_count(self):
        return "%d%%" % self.configuration.candidatos.count() * 100 / 400 if hasattr(self, 'candidatos') else 0

    usage_count.short_description = 'Uso'


class Configuration(models.Model):
    server = models.OneToOneField(Server, on_delete=models.CASCADE)
    candidatos = models.ManyToManyField(
        Candidato,
        blank=True,
        default=None
    )
    keywords = models.ManyToManyField(
        Keyword,
        blank=True,
        default=None
    )

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciónes"

    def __str__(self):
        return self.server.__str__()

    def lista_candidatos(self):
        if self.candidatos:
            return '%s' % ", ".join([candidato.name for candidato in self.candidatos.all().order_by('name')])

    def lista_screen_names(self):
        if self.candidatos:
            return '@%s' % ", @".join([candidato.screen_name for candidato in self.candidatos.all().order_by('name')])

    def lista_keywords(self):
        if self.keywords:
            return '%s' % ", ".join([keyword.name for keyword in self.keywords.all().order_by('name')])


class ConfigurationSync(models.Model):
    STATUS_OK = 'OK'
    STATUS_UNKNOWN = 'UN'
    STATUS_UNKNOWN_RESPONSE = 'UK'
    STATUS_ERROR = 'ER'
    STATUS_CHOICES = (
        (STATUS_OK, 'Sincronizado'),
        (STATUS_UNKNOWN, 'Desconocido'),
        (STATUS_UNKNOWN_RESPONSE, 'Respuesta Erronea'),
        (STATUS_ERROR, 'Falló')
    )
    configuration = models.OneToOneField(Configuration, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Creado", auto_now_add=True)
    modified_at = models.DateTimeField("Modificado", auto_now=True)
    status = models.CharField(
        "Sincronización",
        max_length=2,
        choices=STATUS_CHOICES,
        default='UN'
    )

    class Meta:
        verbose_name = "Sincronización de Configuración"
        verbose_name_plural = "Sincronización de Configuraciones"

    def __str__(self):
        return self.configuration.__str__()
