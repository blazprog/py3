from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View, ListView, UpdateView, CreateView, DeleteView, TemplateView
from .forms import ArtikelForm, SkupinaArtiklaForm, StrankaForm 
#        RacunForm, RacunPozicijaForm, RacunPozicijaFormset)
from .models import Artikel, SkupinaArtikla,Stranka
    
# Create your views here.
def index(request):
    return render(request,"common/base.html")


class ArtikelListView(ListView):
    context_object_name = "seznam_artiklov"
    template_name = "sifranti/seznam_artiklov.html"
    model = Artikel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seznam_skupin_artiklov"] = SkupinaArtikla.objects.all()
        context["aktivna_skupina"] = int(self.kwargs.get("skupina","0"))
        return context

    def get_queryset(self):
        skupina_artikla = self.kwargs.get("skupina","")
        if skupina_artikla:
            skupina_obj = get_object_or_404(SkupinaArtikla,pk=skupina_artikla)
            return Artikel.objects.filter(skupina = skupina_obj)
        else:
            return Artikel.objects.all()


class ArtikelUpdateView(UpdateView):
    model = Artikel
    form_class = ArtikelForm
    template_name = "sifranti/ArtikelForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = reverse("artikel_edit", kwargs= {"pk":self.object.id})
        return context

    def get_success_url(self):
        return reverse("seznam_artiklov")

class ArtikelCreateView(CreateView):
    model = Artikel
    form_class = ArtikelForm
    template_name = "sifranti/ArtikelForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = reverse("artikel_add")
        return context

    def get_success_url(self):
        return reverse("seznam_artiklov")


class ArtikelDeleteView(DeleteView):
    model = Artikel
    template_name = 'sifranti/stranka_delete.html'

    def get_success_url(self):
        return reverse("seznam_artiklov")

class SkupinaArtiklaListView(ListView):
    context_object_name = "seznam_skupin_artiklov"
    template_name = "sifranti/seznam_skupin_artiklov.html"
    model = SkupinaArtikla


class SkupinaArtiklavMixin:
    """
    Funkcije, ki so skupne za UpdeateView in CreateView
    """
    model = SkupinaArtikla
    form_class = SkupinaArtiklaForm
    template_name = "sifranti/SkupinaForm.html"

    def get_success_url(self):
        return reverse("seznam_skupin_artiklov")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if type(self) is SkupinaArtiklaUpdateView:
            context["action"] = reverse("skupina_artikla_edit",
                                kwargs = {"pk": self.object.id})
        else:
            context["action"] = reverse("skupina_artikla_add")
        return context


class SkupinaArtiklaUpdateView(SkupinaArtiklavMixin,UpdateView):
    pass

class SkupinaArtiklaCreateView(SkupinaArtiklavMixin,CreateView):
    pass


class SkupinaArtiklaDeleteView(DeleteView):
    model = SkupinaArtikla
    template_name = 'sifranti/stranka_delete.html' #template mogoce sploh ni pomemben

    def get_success_url(self):
        return reverse("seznam_skupin_artiklov")


class StrankaListView(ListView):
    context_object_name = "seznam_strank"
    template_name = "sifranti/seznam_strank.html"
    model = Stranka 

    def get_queryset(self):
        sifra = self.request.GET.get('sifra')
        naziv = self.request.GET.get("naziv","")
        posta = self.request.GET.get('posta')
        ulica = self.request.GET.get('ulica')
        kraj = self.request.GET.get('kraj')
        if sifra:
            return Stranka.objects.filter(sifra = sifra)     
        elif naziv:
            return Stranka.objects.filter(naziv__startswith = naziv)     
        elif posta:
            return Stranka.objects.filter(posta__startswith = posta)     
        elif ulica:
            return Stranka.objects.filter(ulica__startswith = ulica)     
        elif kraj:
            return Stranka.objects.filter(kraj__startswith = kraj)     
        else:
            return Stranka.objects.all()

class StrankeMixin:
    """
    Funkcije, ki so skupne za UpdeateView in CreateView
    """
    model = Stranka
    form_class = StrankaForm
    template_name = "sifranti/StrankaForm.html"

    def get_success_url(self):
        return reverse("seznam_strank")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if type(self) is StrankaUpdateView:
            context["action"] = reverse("stranka_edit",
                                kwargs = {"pk": self.object.id})
        else:
            context["action"] = reverse("stranka_add")
        return context


class StrankaUpdateView(StrankeMixin,UpdateView):
    pass

class StrankaCreateView(StrankeMixin,CreateView):
    pass


class StrankaDeleteView(DeleteView):
    model = Stranka
    template_name = 'sifranti/stranka_delete.html'

    def get_success_url(self):
        return reverse("seznam_strank")
