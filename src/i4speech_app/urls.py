# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='help'),
    url(r'^textos/$', views.TextosListView.as_view(), name='textos'),
    url(r'^nuevotexto/$', views.TextoNuevoView, name='nuevotexto'),
    url(r'^autores/$', views.AutoresListView.as_view(), name='autores'),
    url(r'^nuevoautor/$', views.AutorNuevoView, name='nuevoautor'),
    url(r'^autores/$', views.AutoresListView.as_view(), name='autores'),
    url(r'^resultados/$', views.ResultadosView, name='resultados'),
    url(r'^resultadoaso/$', views.ResultadoasoView, name='resultadoaso'),
    url(r'^dashboard/$', views.DashboardView, name='dashboard'),
    url(r'^textodetalle/?P<pk>', views.TextoDetailView.as_view(), name='textodetalle'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

