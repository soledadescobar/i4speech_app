# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory


class APIConfigForm(forms.Form):
    keywords = forms.CharField()
    user_ids = forms.CharField()