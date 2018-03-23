# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Textos, Autores, Escalafh, Escalagu, Escalain, Escalamu, Escalasp, Fh, Gu, Mu, Sp, Cr, Ocasiones


@admin.register(Fh)
class FhAdmin(admin.ModelAdmin):
    pass


@admin.register(Gu)
class GuAdmin(admin.ModelAdmin):
    pass


@admin.register(Mu)
class MuAdmin(admin.ModelAdmin):
    pass


@admin.register(Sp)
class SpAdmin(admin.ModelAdmin):
    pass


@admin.register(Cr)
class CrAdmin(admin.ModelAdmin):
    pass


@admin.register(Autores)
class AutoresAdmin(admin.ModelAdmin):
    pass

@admin.register(Textos)
class TextosAdmin(admin.ModelAdmin):
    pass


@admin.register(Escalafh)
class EscalafhAdmin(admin.ModelAdmin):
    pass


@admin.register(Escalain)
class EscalainAdmin(admin.ModelAdmin):
    pass


@admin.register(Escalagu)
class EscalaguAdmin(admin.ModelAdmin):
    pass


@admin.register(Escalasp)
class EscalaspAdmin(admin.ModelAdmin):
    pass


@admin.register(Escalamu)
class EscalamuAdmin(admin.ModelAdmin):
    pass


@admin.register(Ocasiones)
class OcasionesAdmin(admin.ModelAdmin):
    pass



