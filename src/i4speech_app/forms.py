# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from i4speech_app.models import Textos, Autores


class DateInput(forms.DateInput):
    input_type = 'date'


class NuevoTextoForm(forms.ModelForm):

    class Meta:
        model = Textos
        fields = ['idautor', 'idocasion' ,'titulo', 'fecha', 'texto']
        localized_fields = ('texto',)
        widgets = {'fecha': DateInput()}

    def __init__(self, *args, **kwargs):
        super(NuevoTextoForm, self).__init__(*args, **kwargs)
        self.fields['idocasion'].label = 'Ocasión'
        self.fields['idautor'].label = 'Autor'


class NuevoAutorForm(forms.ModelForm):

    class Meta:
        model = Autores
        fields = ['nombre', 'twitter']
