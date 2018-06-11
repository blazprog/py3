from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import PhotoForm
from .models import Photo

def add_picture(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            word = form.save()
            print(word.id)
            return HttpResponseRedirect(reverse("pictures:list_pictures"))
        else:
            print(form.errors)
    else: # GET
        form = PhotoForm()

    context = {"form" : form}
    return render(request,"slike/add_picture.html", context)



def list_pictures(request):
    photos = Photo.objects.order_by("description")
    context_dict = {"photos" : photos}
    return render(request,"slike/album.html", context_dict)





