from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    #return render(request,"besede/blasting_off.html")
    return render(request,"besede/beseda.html")

