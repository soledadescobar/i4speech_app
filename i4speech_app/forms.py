from django import forms
from .models import Textos
from .models import Autores
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = 'date'

class NuevoTextoForm(ModelForm):

    class Meta:
        model = Textos
        fields = ['idautor','idocasion' ,'titulo', 'fecha', 'texto']
        localized_fields = ('texto',)
        widgets = {'fecha': DateInput()}

    def __init__(self, *args, **kwargs):
        super(NuevoTextoForm, self).__init__(*args, **kwargs)
        self.fields['idocasion'].label = 'Ocasión'
        self.fields['idautor'].label = 'Autor'

class NuevoAutorForm(ModelForm):

    class Meta:
        model = Autores
        fields = ['nombre', 'twitter']
