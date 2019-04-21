from django.forms import ModelForm
from polls.models import Data
from django import forms

class DataForm(ModelForm):

    class Meta:
        model = Data
        fields = ('name', 'DateOfBirth',)

