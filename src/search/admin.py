# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class TweetResultsInline(admin.TabularInline):
    model = TweetResult

    fields = ('result_id', 'screen_name')

    readonly_fields = ('result_id', 'screen_name')

    can_delete = False


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):

    list_display = ('term', 'raw_query', 'results_count', 'since_id', 'max_id')

    inlines = [
        TweetResultsInline
    ]

    fieldsets = (
        (
            None, {
                'fields': ('term', 'raw_query', 'max_results', 'results_count')
            }
        ),
        (
            'Opcionales', {
                'fields': ('since', 'until', 'since_id', 'max_id')
            }
        )
    )

    readonly_fields = ('results_count',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + tuple([item.name for item in obj._meta.fields])
        return self.readonly_fields

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(TweetAdmin, self).change_view(request, object_id, extra_context=extra_context)