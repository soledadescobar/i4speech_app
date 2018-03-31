"""i4Speech_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, url
    2. Add a URL to urlpatterns:  url('blog/', include('blog.urls'))
"""

from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static, url
from i4speech.settings import DEBUG

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^textos/$', views.TextosListView.as_view(), name='textos'),
    url(r'^nuevotexto/$', views.TextoNuevoView, name='nuevotexto'),
    url(r'^autores/$', views.AutoresListView.as_view(), name='autores'),
    url(r'^nuevoautor/$', views.AutorNuevoView, name='nuevoautor'),
    url(r'^autores/$', views.AutoresListView.as_view(), name='autores'),
    url(r'^resultados/$', views.ResultadosView, name='resultados'),
    url(r'^resultadoaso/$', views.ResultadoasoView, name='resultadoaso'),
    """url(r'^textodetalle/?P(<pk>)$', views.TextoDetailView.as_view(), name='textodetalle'),""",
    url(r'^dashboard/$', views.DashboardView, name='dashboard'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
