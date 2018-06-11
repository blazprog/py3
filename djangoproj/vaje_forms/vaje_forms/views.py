__author__ = 'blazko'
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def home(request):
    return render(request,"myforms/select_language.html")
