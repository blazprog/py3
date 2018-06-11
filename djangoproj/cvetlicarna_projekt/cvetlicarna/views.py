from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView

from .forms import ArtikelForm, StrankaForm, RacunForm, RacunFormset
from .models import Artikel, Stranka, Racun

def index(request):
    return render(request,"cvetlicarna/index.html")

def dodaj_artikel(request):
    if request.method == "POST":
        form = ArtikelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("cvetlicarna:seznam_artiklov"))

    else:
        form = ArtikelForm()

    return render(request, "cvetlicarna/artikel_form.html",
                  {"form": form, "action": "dodaj_artikel"})


def dodaj_stranko(request):
    if request.method == "POST":
        form = StrankaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("cvetlicarna:seznam_strank"))
    else:
        form = StrankaForm()

    return render(request, "cvetlicarna/stranka_form.html",
                    {"form" : form, "action": "dodaj_stranko"} )

def dodaj_racun(request):
    if request.method == "POST":
        racun = RacunForm(request.POST)
        racunFormset = RacunFormset(request.POST)
        if racun.is_valid():
            racun_model = racun.save()
            print("Racun je shranjen")
            if racunFormset.is_valid():
                instances = racunFormset.save(commit=False)
                for instance in instances:
                    instance.idRacuna = racun_model
                    instance.save()

                return HttpResponseRedirect(reverse("cvetlicarna:seznam_racunov"))
    else:
        racun = RacunForm()
        racunFormset = RacunFormset()

    return render(request, "cvetlicarna/racun_form.html",
                    {"form": racun, "formset" : racunFormset,
                     "action" : reverse("cvetlicarna:dodaj_racun")})

def uredi_racun(request, pk):
    obj_racun = Racun.objects.get(pk=int(pk))
    if request.method == "POST":
        racun = RacunForm(request.POST, instance=obj_racun)
        racunFormset = RacunFormset(request.POST, instance=obj_racun)
        if racun.is_valid():
            racun_model = racun.save()
            print("Racun je shranjen")
            if racunFormset.is_valid():
                instances = racunFormset.save(commit=False)
                stevilkaPostavke = 1
                for instance in instances:
                    instance.idRacuna = racun_model
                    instance.stevilkaPostavke = stevilkaPostavke
                    stevilkaPostavke += 1
                    instance.save()
                return HttpResponseRedirect(reverse("cvetlicarna:seznam_racunov"))
            else:
                print(racunFormset.errors)
        else:
            print(racun.errors)
    else:
        racun = RacunForm(instance=obj_racun)
        racunFormset = RacunFormset(instance=obj_racun)

    return render(request, "cvetlicarna/racun_form.html",
                    {"form": racun, "formset" : racunFormset,
                     "action" : reverse("cvetlicarna:uredi_racun", kwargs={"pk": int(pk)})})



class SeznamArtiklov(ListView):
    model = Artikel
    template_name = "cvetlicarna/seznam_artiklov.html"

class SeznamStrank(ListView):
    model = Stranka
    template_name = "cvetlicarna/seznam_strank.html"

class SeznamRacunov(ListView):
    model = Racun
    template_name = "cvetlicarna/seznam_racunov.html"

class UpdateArtikelView(UpdateView):
    model = Artikel
    template_name = "cvetlicarna/artikel_form.html"
    form_class = ArtikelForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = reverse("cvetlicarna:uredi_artikel",
                kwargs = {'pk': self.get_object().id})

        return context

    def get_success_url(self):
        return reverse("cvetlicarna:seznam_artiklov")


class UpdateStrankaView(UpdateView):
    model = Stranka
    template_name = "cvetlicarna/stranka_form.html"
    form_class = StrankaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = reverse("cvetlicarna:uredi_stranko",
                                    kwargs = {'pk': self.get_object().id})

        return context


    def get_success_url(self):
        return reverse("cvetlicarna:seznam_strank")



def get_artikel_details(request):
    if request.method == "GET":
        sifraArtikla = request.GET["sifraArtikla"]
        artikel = Artikel.objects.get(pk=int(sifraArtikla))
        data = {"cena": artikel.cena,
                "idEm": artikel.idEm.id,
                "idDDV": artikel.idDDV.id}
        return JsonResponse(data)

