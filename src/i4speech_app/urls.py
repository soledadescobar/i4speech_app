# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='help'),
    url('^textos/$', views.TextosListView.as_view(), name='textos'),
    url('^nuevotexto/$', views.TextoNuevoView, name='nuevotexto'),
    url('^autores/$', views.AutoresListView.as_view(), name='autores'),
    url('^nuevoautor/$', views.AutorNuevoView, name='nuevoautor'),
    url('^autores/$', views.AutoresListView.as_view(), name='autores'),
    url('^resultados/$', views.ResultadosView, name='resultados'),
    url('^resultadoaso/$', views.ResultadoasoView, name='resultadoaso'),
    url('^textodetalle/(<pk>)', views.TextoDetailView.as_view(), name='textodetalle'),
    url('^dashboard/$', views.DashboardView, name='dashboard'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

