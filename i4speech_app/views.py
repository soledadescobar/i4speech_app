from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Textos, Autores, Escalafh, Escalamu, Escalasp, Escalagu, Escalain, Cr, Fh, Gu, Mu, Sp
from django.views import generic
from django.forms import ModelForm
from .forms import NuevoTextoForm
from .forms import NuevoAutorForm
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.db.models import Avg
from .chartdata import ChartData


def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_textos = Textos.objects.all().count()
    num_autores = Autores.objects.all().count()


    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'i4speech_app/index.html',
        context={'num_textos': num_textos, 'num_autores': num_autores,},
    )

class TextosListView(generic.ListView):
    model = Textos


class AutoresListView(generic.ListView):
    model = Autores
    num_textos = Textos.objects.all().count()
    prom_cr = Cr.objects.values('idtexto__idautor__nombre').annotate(prom_cr=Avg('resultado')).order_by('idtexto__idautor__nombre')

class TextoDetailView(generic.DetailView):
    model = Textos


def TextoNuevoView(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = NuevoTextoForm(request.POST or None)
        # Check if the form is valid:
        if form.is_valid():
            form.save()
            form = NuevoTextoForm()
    # If this is a GET (or any other method) create the default form.

    else:
        form = NuevoTextoForm()
    return render(request, 'i4speech_app/nuevo_texto.html', {'form': form})


def AutorNuevoView(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = NuevoAutorForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            form.save()
            form = NuevoAutorForm()
    # If this is a GET (or any other method) create the default form.
    else:
        form = NuevoAutorForm()
    return render(request, 'i4speech_app/nuevo_autor.html', {'form': form})


def ResultadosView (request):
    return render(request, 'i4speech_app/resultados.html')

def ResultadoasoView (request):
    return render(request, 'i4speech_app/resultadoaso.html')


def DashboardView(request, chartID='chart_ID', chart_type='column', chart_height=500):
    data = ChartData.todos_los_promedios()

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text": 'Promedio por autor y tipo de índice'}
    xAxis = {"title": {"text": 'Autor'}, "categories": data['autor']}
    yAxis = {"title": {"text": 'Valor'}}

    series = [
        {"name": 'SP', "data": data['sp']},
        {"name": 'FH', "data": data['fh']},
        {"name": 'GU', "data": data['gu']},
        {"name": 'MU', "data": data['mu']},
        {"name": 'CR', "data": data['cr']}
    ]

    return render(request, 'i4speech_app/dashboard.html', {'chartID': chartID, 'chart': chart,
                                                    'series': series, 'title': title,
                                                    'xAxis': xAxis, 'yAxis': yAxis})
