from django.shortcuts import render
from django.http import HttpResponse
from .Forms import DataForm
from .models import Data

# Create your views here.
def home_view(request): # *args, **kwargs
    return render(request, "polls/home.html", {})

def project_list_view(request):
    queryset = Data.objects.all()  # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, "polls/project-list.html", context)

def data_create_view(request):
    form = DataForm(request.POST)
    if form.is_valid():
        form.save()
    context = {
        'form' : form
    }
    return render(request, "polls/data_create.html", context)

def polls_detail_view(request, id):
    obj = Data.objects.get(id=1)
    context = {
        "object": obj
    }
    return render(request, "polls/polls_detail.html", context)