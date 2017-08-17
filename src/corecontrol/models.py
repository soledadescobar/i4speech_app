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


class InstanceTypes(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Instances(models.Model):
    name = models.CharField(max_length=50)
    ip = models.CharField(max_length=50)
    it = models.ForeignKey(InstanceTypes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ApiKey(models.Model):
    name = models.CharField(max_length=10)
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
    apikey = models.ForeignKey(ApiKey, on_delete=models.CASCADE)

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


class Configuration(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    candidatos = models.ManyToManyField(Candidato)
    keywords = models.ManyToManyField(Keyword)

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
