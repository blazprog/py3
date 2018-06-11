from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import View, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import json
from .models import Racun, RacunPozicija,RacunRekapitulacija, getNextDocumentNumber
from sifranti.models import Artikel, Stranka
from .forms import RacunForm,RacunPozicijaFormset
import codecs
from .directsql import getJsonArtikel, getSkupineArtiklov
from .serializer import StrankaSerializer, ArtikelSerializer


def racuni(request):
    return HttpResponse('Si v aplikaciji dokumenti')


class PotrditevVnosaRacuna(TemplateView):
    template_name = 'dokumenti/racun_preview.html'

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
        return render(request,"dokumenti/racun_add.html",
                      {"form_master" : form_master,
                       "form_detail" : form_detail,
                       "action" : reverse("racun_add")}
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
                return render(request,"dokumenti/racun_add.html",
                    {"form_master" : form_master,
                    "form_detail" : form_detail,
                     "action" : reverse("racun_add")}
                     )

            #both forms are valid
            return HttpResponseRedirect(reverse("racun_view",kwargs={'pk':form_model.id}))

        else: #form_master is invalid
            print("Erros occured")
            return render(request,"dokumenti/racun_add.html",
              {"form_master" : form_master,
               "form_detail" : form_detail,
                "action" : reverse("racun_add")})



              
class RacunUpdateView(View):
    def get(self, request,pk, *args, **kwargs):
        racun = get_object_or_404(Racun,pk=pk)
        initial_data = {'txtSifraStranke':racun.stranka.sifra, 'txtNazivStranke':racun.stranka.naziv}
        form_master = RacunForm(instance = racun, initial = initial_data)
        form_detail = RacunPozicijaFormset(instance=racun)
        return render(request,"dokumenti/racun_add.html",
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
                return render(request,"dokumenti/racun_add.html",
                    {"form_master" : form_master,
                    "form_detail" : form_detail,
                     "action" : reverse("racun_eidt,kwargs={'pk':pk}")})

            return HttpResponseRedirect(reverse("racun_view",kwargs={'pk':form_model.id}))
        else:
            print("Erros occured")
            return render(request,"dokumetni/racun_add.html",
              {"form_master" : form_master,
               "form_detail" : form_detail,
                "action" : reverse("racun_edit",kwargs={'pk':pk})})


class SeznamRacunov(ListView):
    queryset = Racun.objects.all().order_by('-stevilka')
    template_name = "dokumenti/seznam_racunov.html"
    context_object_name = 'seznam_racunov'



class SeznamDokumentov(TemplateView):
    template_name = "dokumenti/seznam_dokumentov.html"



class AjaxView(View):
    def get(self, request):
        return render(request,"dokumenti/ajax.html")

class GridView(View):
    def get(self, request):
        return render(request,"dokumenti/grid.html")

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

        return render_to_response('dokumenti/lookup_artikel.html',
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
        template_name = 'dokumenti/searchResult_artikel.html'
    elif table.lower() == 'stranka':
        model_search = Stranka
        template_name = "dokumenti/searchResult_stranka.html"

    search_string = request.GET["q"]
    context_list = model_search.objects.filter(naziv__icontains=search_string)
    if context_list:
        if len(context_list) > 12:
            context_list = context_list[:12]

    return render_to_response(template_name,
                              {'context_list': context_list}) 

@csrf_exempt
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
    elif request.method == 'POST': 
        #for debug
        print("Post values")
        print(type(request.POST),request.POST)
        for key in request.POST:
            value = request.POST[key]
            print (key ,value)
        dataIn = request.POST.dict()
        print(type(dataIn),dataIn)
        data = {'ok': 'Es ist ok'}
        return JsonResponse(data)


def get_artikel_by_id(request):
    if request.method == 'GET':
        idArtikla = request.GET['q']
        data = getJsonArtikel(idArtikla)
        return JsonResponse(data[0])
    

def get_skupina_artiklov(request):
    if request.method == 'GET':
        data = getSkupineArtiklov()
        return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
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
    
class TodoExercise(TemplateView):
    template_name = 'dokumenti/todo.html'


class StrankeList(APIView):
    def get(self, request, format=None):
        print('getting stranka')
        stranke = Stranka.objects.all()
        serializer = StrankaSerializer(stranke, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print('Posting stranka')
        serializer = StrankaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)


class StrankaDetail(APIView):
    def get_object(self, pk):
        try:
            return Stranka.objects.get(pk=pk)
        except Stranka.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        stranka = self.get_object(pk)
        serializer = StrankaSerializer(stranka)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        stranka = self.get_object(pk)
        serializer = StrankaSerializer(stranka, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        stranka = self.get_object(pk)
        stranka.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ArtikelList(APIView):
    def get(self, request, format=None):
        artikels = Artikel.objects.all()
        serializer = ArtikelSerializer(artikels, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArtikelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           

class ArtikelDetail(APIView):
    def get_object(self, pk):
        try:
            return Artikel.objects.get(pk=pk)
        except Artikel.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        artikel = self.get_object(pk)
        serializer = ArtikelSerializer(artikel)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        artikel = self.get_object(pk)
        serializer = ArtikelSerializer(artikel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        artikel = self.get_object(pk)
        artikel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



            

