# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
import requests
from .models import *
from control.models import Keyword, Candidato
from django.contrib.auth.decorators import login_required


class ConfigurationsListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    model = Configuration

    template_name = 'corecontrol/configuration.html'

    context_object_name = 'configurations'

    queryset = Configuration.objects.prefetch_related('keywords', 'candidatos')

    def get_context_data(self, **kwargs):

        context = super(ConfigurationsListView, self).get_context_data(**kwargs)

        context['keywords'] = Keyword.objects.all().order_by('name')

        context['candidatos'] = Candidato.objects.all().order_by('name')

        return context


class ServersListView(LoginRequiredMixin, ListView):
    model = Server

    template_name = 'corecontrol/status.html'

    context_object_name = 'servers'

    def get_context_data(self, **kwargs):

        context = super(ServersListView, self).get_context_data(**kwargs)

        context['sync'] = {}

        for server in context['servers']:
            config = Configuration.objects.filter(server=server).get()
            context['sync'][server] = config.configurationsync.get_status_display()

        return context


@login_required
def get_server_status(request, pk):
    server = Server.objects.filter(id=pk).get()
    r = requests.get(
        "http://%s:5000/status" % server.ip,
        auth=('admin', 'secret'),
        timeout=5
    )
    if r.status_code == 200:
        return HttpResponse('OK')
    else:
        return Http404


@login_required
def restart_server(request, pk):
    server = Server.objects.filter(id=pk).get()
    r = requests.get(
        "http://%s:5000/update" % server.ip,
        auth=('admin', 'secret'),
        timeout=5
    )
    if r.status_code == 200:
        return HttpResponse('OK')
    else:
        return Http404
