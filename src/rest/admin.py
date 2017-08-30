# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.


class QueryParamInLine(admin.TabularInline):
    model = QueryParam


class QueryValueInLine(admin.TabularInline):
    model = QueryValue


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'joined_params', 'joined_values')

    search_fields = ['name']

    inlines = [
        QueryParamInLine,
        QueryValueInLine
    ]


class ModelJoinFieldInLine(admin.TabularInline):
    model = ModelJoinField


@admin.register(ModelJoin)
class ModeljoinAdmin(admin.ModelAdmin):
    list_display = ('model', 'webservice', 'name', 'field', 'param')

    inlines = [
        ModelJoinFieldInLine
    ]


class ModelCustomFilterFieldInLine(admin.TabularInline):
    model = ModelCustomFilterField


@admin.register(ModelCustomFilter)
class ModelCustomFilterAdmin(admin.ModelAdmin):
    list_display = ('model',)

    inlines = [
        ModelCustomFilterFieldInLine
    ]
