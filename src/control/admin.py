# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ['keyword__name']


@admin.register(Posicion)
class PosicionAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ['posicion__name']


@admin.register(Frente)
class FrenteAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ['frente__name']


@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'frente')

    list_filter = ('frente',)

    search_fields = ['bloque__name', 'frente__name']


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ['provincia__name']


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_select_related = (
        'bloque',
        'bloque__frente',
    )

    list_display = ('name', 'screen_name_url', 'bloque', 'provincia')

    search_fields = ['candidato__name', 'candidato__screen_name', 'bloque__name', 'provincia__name']

    list_filter = ('provincia', 'bloque')

    readonly_fields = ['screen_name_url']

    fieldsets = (
        (None, {
            'fields': ('name', 'screen_name_url')
        }),
        ('Datos para Gráficos', {
            'fields': ('bloque', 'provincia')
        })
    )

    def screen_name_url(self, obj):
        return '<a href="https://twitter.com/intent/user?user_id={}" target="_blank">{}</a>'.format(
            obj.user_id, obj.screen_name
        )
    screen_name_url.short_description = "Screen Name"
    screen_name_url.allow_tags = True


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'candidato',
        'frente',
        'bloque',
        'provincia')

    search_fields = [
        'lista__name',
        'candidato__name',
        'candidato__screen_name',
        'frente__name',
        'bloque__name',
        'provincia__name']

    list_filter = ('provincia', 'frente', 'bloque')

