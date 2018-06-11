from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, UpdateView, CreateView
from django.views.generic import View, TemplateView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.


class IndexView(TemplateView):
    template_name = 
    return render(request,"lab/index.html")

