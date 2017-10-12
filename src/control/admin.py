# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.utils.text import force_text
from .models import *

# from django_extensions.admin import ForeignKeyAutocompleteAdmin


def rest_make_visible(modeladmin, request, queryset):
    queryset.update(rest_visible=True)


rest_make_visible.short_description = "[REST] Hacer Visible(s)"


def rest_make_invisible(modeladmin, request, queryset):
    queryset.update(rest_visible=False)


rest_make_invisible.short_description = "[REST] Hacer Invisible(s)"


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
    list_display = ('name', 'display_color', 'rest_visible')

    search_fields = ['name']

    readonly_fields = ['display_color']

    list_filter = ('rest_visible',)

    actions = [rest_make_visible, rest_make_invisible]

    def display_color(self, obj):
        return '<span style="background: #{};">&nbsp;{}&nbsp;</span>'.format(
            obj.color, obj.color
        )
    display_color.short_description = "Color"
    display_color.allow_tags = True


@admin.register(Bloque)
class BloqueAdmin(admin.ModelAdmin):
    list_select_related = ('frente', 'provincia')

    related_search_fields = {
        'frente': ('name',),
        'provincia': ('name',),
    }

    list_display = ('name', 'frente', 'display_color', 'rest_visible')

    list_filter = ('frente', 'rest_visible')

    search_fields = ['bloque__name', 'frente__name']

    actions = [rest_make_visible, rest_make_invisible]

    def display_color(self, obj):
        return '<span style="background: #{};">&nbsp;{}&nbsp;</span>'.format(
            obj.frente.color, obj.frente.color
        )
    display_color.short_description = "Color del Frente"
    display_color.allow_tags = True


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ['provincia__name']


@admin.register(Distrito)
class DistritoAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ['distrito__name']


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_select_related = (
        'bloque',
        'frente',
        'provincia',
        'distrito',
        'posicion'
    )

    related_search_fields = {
        'bloque': ('name',),
        'frente': ('name',),
        'provincia': ('name',),
        'distrito': ('name',),
        'posicion': ('name',),
    }

    list_display = ('name', 'screen_name_url', 'posicion', 'provincia', 'frente', 'bloque', 'rest_visible')

    search_fields = ['name', 'screen_name']

    list_filter = ('rest_visible', 'provincia', 'posicion', 'frente', 'bloque', 'distrito')

    readonly_fields = ['screen_name_url']

    actions = [rest_make_visible, rest_make_invisible]

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Datos Politicos', {
            'fields': ('frente', 'bloque', 'posicion', 'provincia', 'distrito')
        }),
        ('Twitter', {
            'fields': ('screen_name', 'screen_name_url')
        }),
        ('WebServices', {
            'fields': ('rest_visible',)
        })
    )

    def screen_name_url(self, obj):
        return '<a href="https://twitter.com/intent/user?user_id={}" target="_blank">{}</a>'.format(
            obj.user_id, obj.screen_name
        )
    screen_name_url.short_description = "Screen Name"
    screen_name_url.allow_tags = True


class ListaSeccionInline(admin.StackedInline):
    model = ListaSeccion

    readonly_fields = ['get_edit_link']

    def get_edit_link(self, obj=None):
        if obj.pk:  # if object has already been saved and has a primary key, show link to it
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[force_text(obj.pk)])
            return """<a href="{url}">{text}</a>""".format(
                url=url,
                text="Editar esta sección",
            )
        return "(Escoja Guardar y Seguir Editando para Cargar datos en esta sección)"
    get_edit_link.short_description = "Link para Editar"
    get_edit_link.allow_tags = True


class ListaSeccionCandidatoInline(admin.StackedInline):
    model = ListaSeccionCandidato


@admin.register(Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'name',
        'provincia')

    search_fields = [
        'lista__name'
        ]

    list_filter = ('provincia',)

    actions = [rest_make_visible, rest_make_invisible]

    inlines = [
        ListaSeccionInline
    ]


@admin.register(ListaSeccion)
class ListaSeccionAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [ListaSeccionCandidatoInline]