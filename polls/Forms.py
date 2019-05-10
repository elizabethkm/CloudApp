from django.forms import ModelForm
from .models import Data
from .models import Data2


class DataForm2(ModelForm):

    class Meta:
        model = Data2
        fields = ('Gender', 'ProcedureType', 'ProcedureReason', 'ProcedureOutcome',)


class DataForm(ModelForm):

    class Meta:
        model = Data
        fields = ('FirstName', 'LastName', 'DateOfBirth', 'Age', 'Gender', 'ProcedureType', 'ProcedureReason', 'ProcedureOutcome',)



