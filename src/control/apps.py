# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ControlConfig(AppConfig):
    name = 'control'
    verbose_name = "Administración de Datos"

    def ready(self):
        import control.signals