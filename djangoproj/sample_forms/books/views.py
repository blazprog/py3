from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import BookForm

def index(request):
    return render(request,"books/index.html")

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("thanks"))
        else:
            print(form.errors)
    else:
        form = BookForm()

    #Vrnem prazno formo, ali pa nepravilno izpolnjeno
    context = {"form" : form}
    return render(request,"books/add_book.html", context)


def thanks(request):
    return render(request,"books/thanks.html")