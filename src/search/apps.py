# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class SearchConfig(AppConfig):
    name = 'search'
    verbose_name = "Búsquedas"

    def ready(self):
        import search.signals