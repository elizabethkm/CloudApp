from django.forms import ModelForm
from polls.models import Data
from django import forms

class DataForm(ModelForm):
    name = forms.CharField(label='Name',
                            widget=forms.TextInput(attrs={"placeholder": "Subject Name"}))

    DateofBirth = forms.CharField(label='Date of Birth',
                            widget=forms.TextInput(attrs={"placeholder": "12-01-1990"}))
#DecimalField(initial= 12011990)
    class Meta:
        model = Data
        fields = [ 'name',
            'DateofBirth']

