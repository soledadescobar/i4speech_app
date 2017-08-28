# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CorecontrolConfig(AppConfig):
    name = 'corecontrol'
    verbose_name = 'Configuraciones'

    def ready(self):
        import corecontrol.signals