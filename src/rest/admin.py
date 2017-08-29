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


admin.site.register(ModelJoin)