from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View, ListView, UpdateView, CreateView, DeleteView, TemplateView

from rest_framework.renderers import JSONRenderer #tega sedaj ne rabim vec, ker uporabljam rest frameworkove metode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .forms import (ArtikelForm, SkupinaArtiklaForm, StrankaForm, 
        RacunForm, RacunPozicijaForm, RacunPozicijaFormset)
from .models import Artikel, SkupinaArtikla, Counter, Stranka, Racun, RacunPozicija, getNextDocumentNumber
from .serializers import StrankaSerializer


def index(request):
    return render(request,"invoices/index.html")

class ArtikelUpdateView(UpdateView):
    model = Artikel
    form_class = ArtikelForm
    template_name = "invoices/ArtikelForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = reverse("artikel_edit", kwargs= {"pk":self.object.id})
        return context

    def get_success_url(self):
        return reverse("seznam_artiklov")

class ArtikelCreateView(CreateView):
    model = Artikel
    form_class = ArtikelForm
    template_name = "invoices/ArtikelForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = reverse("artikel_add")
        return context

    def get_success_url(self):
        return reverse("seznam_artiklov")


class ArtikelListView(ListView):
    context_object_name = "seznam_artiklov"
    template_name = "invoices/seznam_artiklov.html"
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


class SkupinaArtiklaListView(ListView):
    context_object_name = "seznam_skupin_artiklov"
    template_name = "invoices/seznam_skupin_artiklov.html"
    model = SkupinaArtikla


class SkupinaArtiklavMixin:
    """
    Funkcije, ki so skupne za UpdeateView in CreateView
    """
    model = SkupinaArtikla
    form_class = SkupinaArtiklaForm
    template_name = "invoices/SkupinaForm.html"

    def get_success_url(self):
        return reverse("seznam_skupin_artiklov")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if type(self) is SkupinaArtiklaUpdateView:
            context["action"] = reverse("s kupina_artikla_edit",
                                kwargs = {"pk": self.object.id})
        else:
            context["action"] = reverse("skupina_artikla_add")
        return context


class SkupinaArtiklaUpdateView(SkupinaArtiklavMixin,UpdateView):
    pass

class SkupinaArtiklaCreateView(SkupinaArtiklavMixin,CreateView):
    pass


class StrankaListView(ListView):
    context_object_name = "seznam_strank"
    template_name = "invoices/seznam_strank.html"
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
    template_name = "invoices/StrankaForm.html"

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
    template_name = 'invoices/stranka_delete.html'

    def get_success_url(self):
        return reverse("seznam_strank")


class PotrditevVnosaRacuna(TemplateView):
    template_name = 'invoices/racun_preview.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pk = kwargs.get('pk')
        racun = get_object_or_404(Racun, pk = pk)
        racun_pozicije = get_list_or_404(RacunPozicija, racun=racun)
        recap = racun.skupniZneski()
        context['racun'] = racun
        context['racun_pozicije'] = racun_pozicije
        context['rekapitulacija'] = recap
        return context

class RacunCreateView(View):
    def get(self, request,*args, **kwargs):
        initial_data = {'prodajni_pogoji': 'Daj kar das!',
                        'kraj_izdaje' : 'Maribor',
                        'datum_izdaje' : date.today(),
                        'datum_storitve' : date.today(),
                        'datum_valute' : date.today() + timedelta(days=30),
                        'prodajalec' : 'Olga Girja',
                        'referenca': 'Ref #',
                        }

        form_master = RacunForm(initial=initial_data)
        form_detail = RacunPozicijaFormset()
        return render(request,"invoices/racun_add.html",
                      {"form_master" : form_master,
                       "form_detail" : form_detail,
                       "action" : reverse("racun_add")},
                      )

    def post(self, request, *args, **kwargs):
        form_master = RacunForm(request.POST)
        form_detail = RacunPozicijaFormset(request.POST)

        if form_master.is_valid():
            form_model = form_master.save(commit=False)
            form_model.stevilka = getNextDocumentNumber('racun')
            form_model.save()
            print("Glava je shranjen")
            if form_detail.is_valid():
                print('Instance is valid')
                instances = form_detail.save(commit=False)
                i=1
                for instance in instances:
                    if instance.artikel:
                        instance.racun = form_model
                        instance.zaporedna_stevilka = i
                        i+=1
                        print(instance.kolicina, instance.cena)
                        instance.save()
            else: #form_detail is invalid
                print("Erros occured")
                print(form_detail.errors)
                return render(request,"invoices/racun_add.html",
                    {"form_master" : form_master,
                    "form_detail" : form_detail,
                     "action" : reverse("racun_add")})

            #both forms are valid
            return HttpResponseRedirect(reverse("racun_view",kwargs={'pk':form_model.id}))

        else: #form_master is invalid
            print("Erros occured")
            return render(request,"invoices/racun_add.html",
              {"form_master" : form_master,
               "form_detail" : form_detail,
                "action" : reverse("racun_add")})



              
class RacunUpdateView(View):
    def get(self, request,pk, *args, **kwargs):
        racun = get_object_or_404(Racun,pk=pk)
        initial_data = {'txtSifraStranke':racun.stranka.sifra, 'txtNazivStranke':racun.stranka.naziv}
        form_master = RacunForm(instance = racun, initial = initial_data)
        form_detail = RacunPozicijaFormset(instance=racun)
        return render(request,"invoices/racun_add.html",
                      {"form_master" : form_master,
                       "form_detail" : form_detail,
                       "action" : reverse("racun_edit",
                                          kwargs={"pk":pk})})

    def post(self, request,pk, *args, **kwargs):
        racun = get_object_or_404(Racun,pk=pk)
        form_master = RacunForm(request.POST, instance=racun)
        form_detail =  RacunPozicijaFormset(request.POST, instance=racun)

        if form_master.is_valid():
            form_model = form_master.save()
            print("Glava je shranjen")
            if form_detail.is_valid():
                instances = form_detail.save(commit=False)
                i=1
                for instance in instances:
                    instance.racun = form_model
                    instance.zaporedna_stevilka = i
                    i+=1
                    instance.save()
            else:
                print("Erros occured")
                print(form_detail.errors)
                return render(request,"invoices/racun_add.html",
                    {"form_master" : form_master,
                    "form_detail" : form_detail,
                     "action" : reverse("racun_eidt,kwargs={'pk':pk}")})

            return HttpResponseRedirect(reverse("racun_view",kwargs={'pk':form_model.id}))
        else:
            print("Erros occured")
            return render(request,"invoices/racun_add.html",
              {"form_master" : form_master,
               "form_detail" : form_detail,
                "action" : reverse("racun_edit",kwargs={'pk':pk})})


class SeznamRacunov(ListView):
    queryset = Racun.objects.order_by('-stevilka')
    template_name = "invoices/seznam_racunov.html"
    context_object_name = "seznam_racunov"



class AjaxView(View):
    def get(self, request):
        return render(request,"invoices/ajax.html")

class GridView(View):
    def get(self, request):
        return render(request,"invoices/grid.html")

def like_click(request):
    if request.method=="GET":
        counter = get_object_or_404(Counter,id=1)
        clicks = counter.num_counts
        counter.num_counts = clicks +1
        counter.save()
        data = {"clicks" : clicks}
        return JsonResponse(data)


def suggest_names(request):
    """Function returns first 12 names that begins with
    given string.
    """
    if request.method == "GET":
        contains = request.GET["q"]
        artikel_list = Artikel.objects.filter(naziv__icontains=contains)
        if artikel_list:
            if len(artikel_list) > 12:
                artikel_list = artikel_list[:12]

        return render_to_response('invoices/lookup_artikel.html',
                                  {'seznam_artiklov': artikel_list}) #,
                                  #context_instance=RequestContext(request))

def get_tabular_template(request, table):
    """Function returns tabular template of table filtered 
    by given query string.
    """

    if request.method != "GET":
        return

    if table.lower() == 'artikel':
        model_search = Artikel
        template_name = 'invoices/searchResult_artikel.html'
    elif table.lower() == 'stranka':
        model_search = Stranka
        template_name = "invoices/searchResult_stranka.html"

    search_string = request.GET["q"]
    context_list = model_search.objects.filter(naziv__icontains=search_string)
    if context_list:
        if len(context_list) > 12:
            context_list = context_list[:12]

    return render_to_response(template_name,
                              {'context_list': context_list}) 



def get_artikel_details(request):

    if request.method == "GET":
        sifraArtikla = request.GET["q"]
        artikel = Artikel.objects.get(sifra=sifraArtikla);
        data = {"sifra": artikel.sifra,
                "idArtikla": artikel.id,
                "naziv": artikel.naziv,
                "davek": artikel.davek,
                "cena": artikel.cena}
        return JsonResponse(data)



def get_stranka_details(request):
    if request.method == "GET":
        sifraStranke = request.GET["q"]
        stranka = Stranka.objects.get(sifra=sifraStranke)

        data = {
                "idStranke": stranka.id,
                "sifraStranke": stranka.sifra,
                "nazivStranke": stranka.naziv,
                "posta": stranka.posta,
                "ulica": stranka.ulica,
                "kraj": stranka.kraj,}
        return JsonResponse(data)



#koda, ki uporablja rest_framework



@api_view(['GET','POST'])
def customer_list(request, format=None):
    if request.method == 'GET':
        stranke = Stranka.objects.all()
        serializer = StrankaSerializer(stranke, many=True)
        #return JSONResponse(serializer.data) ker uporabljan rest framework response
        #sedaj ne rabim vec sam pretvarjati podatke v JSON
        return Response(serializer.data)


@api_view(['GET','PUT','DELETE'])
def customer_details(request,sifra, format=None):
    try:
        stranka = Stranka.objects.get(sifra=sifra)
    except Stranka.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    except Stranka.MultipleObjectsReturned:
        return HttpResponse('More than one costumer exists')


    if request.method == 'GET':
        serializer = StrankaSerializer(stranka)
        return Response(serializer.data)
    
