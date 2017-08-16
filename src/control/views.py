# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


class CandidatosListView(ListView):
    model = Candidato

    template_name = 'corecontrol/candidatos.html'

    context_object_name = 'candidatos'


