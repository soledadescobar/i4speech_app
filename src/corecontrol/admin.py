# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Instances)


def ConfigurationSyncListInLine(obj):
    sync = ConfigurationSync.objects.filter(configuration=obj).get()
    return sync.get_status_display()
ConfigurationSyncListInLine.short_description = "Sincronización"


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):

    list_display = ('server', ConfigurationSyncListInLine, 'lista_keywords', 'lista_screen_names')

    search_fields = ['server__name', 'keywords__name', 'candidatos__name']


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'server_type', 'ip', 'apikey')

    search_fields = ['server__name', 'server__ip']

    list_filter = ('server_type',)


@admin.register(ServerType)
class ServerTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

    search_fields = ['server_type__name']


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'consumer_key',
        'consumer_secret',
        'api_key',
        'api_secret')

    search_fields = [
        'apikey__name',
        'apikey__consumer_key',
        'apikey__consumer_secret',
        'apikey__api_key',
        'apikey__api_secret']
