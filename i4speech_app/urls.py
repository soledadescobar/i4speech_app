"""i4Speech_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from i4speech.settings import DEBUG

urlpatterns = [
    path('', views.index, name='index'),
    path('textos/', views.TextosListView.as_view(), name='textos'),
    path('nuevotexto/', views.TextoNuevoView, name='nuevotexto'),
    path('autores/', views.AutoresListView.as_view(), name='autores'),
    path('nuevoautor/', views.AutorNuevoView, name='nuevoautor'),
    path('autores/', views.AutoresListView.as_view(), name='autores'),
    path('resultados/', views.ResultadosView, name='resultados'),
    path('resultadoaso/', views.ResultadoasoView, name='resultadoaso'),
    path('textodetalle/(<pk>)/', views.TextoDetailView.as_view(), name='textodetalle'),
    path('dashboard', views.DashboardView, name='dashboard'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
