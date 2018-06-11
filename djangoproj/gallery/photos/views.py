from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, UpdateView, CreateView
from django.views.generic import View, TemplateView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Car
from .forms import CarForm

# Create your views here.


class IndexView(TemplateView):
    template_name = 'photos/index.html' 


class CarsView(TemplateView):
    template_name = 'photos/cars.html'


    
class CarsCreateView(CreateView):
    model = Car
    form_class = CarForm 
    template_name = "photos/CarsForm.html"


    def get_success_url(self):
        return reverse("cars_gallery")
