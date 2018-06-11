
from django.shortcuts import render, get_object_or_404
#from django.views.generic import View, ListView, UpdateView, CreateView
from django.views.generic import View, TemplateView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import (NameForm, ContactMeForm, ArticleForm, ArticleFormSet,ArticleFormSetHelper,NakupIzdelkiFormSetHelper,
                     NakupForm, NakupIzdelkiForm, NakupIzdelkiFormset)
from .models import Nakup, NakupIzdelki

from crispy_forms.layout import Submit, Layout, Field,Div,Fieldset,HTML, Button
from .lookup import slovene_deutsch

# Create your views here.
def index(request):
    return render(request,"lab/index.html")


class NameView(View):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}
        self.context["action"] = reverse("enter_name")

    def get(self,request,*args, **kwargs):
        form = NameForm()
        self.context["form"] = form
        return render(request,"lab/name.html",self.context)


    def post (self, request, *args, **kwargs):
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("index"))
        else:
            self.context["form"] = form
            return render(request,"lab/name.html",self.context)


class ContactMeView(View):

    def __init__(self, *args, **kwargs):
        print(kwargs)
        self.context = {}
        self.context["action"] = reverse("contact_me")

    def get(self,request, *args, **kwargs):
        form = ContactMeForm()
        self.context["form"] = form
        return render(request,"lab/contact_me.html", self.context)

    def post(self, request, *args, **kwargs):
        form = ContactMeForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["subject"])
            return HttpResponseRedirect(reverse("index"))
        else:
            self.context["form"] = form
            return render(request, "lab/contact_me.html", self.context)

class EditArticlesView(View):

    def get(self,request, *args, **kwargs):
        formset = ArticleFormSet()
        #helper = ArticleFormSetHelper()
        #helper.add_input(Submit("submit","Save"))

        #helper.template = "bootstrap/table_inline_formset.html"
        #return render(request, "lab/articles_crispy.html", {"formset": formset,
        #                                                    "helper" : helper})
        return render(request, "lab/articles.html", {"formset": formset})

    def post(self, request, *args, **kwargs):
        formset = ArticleFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    print(form.cleaned_data["title"], form.cleaned_data["pub_date"])
                except KeyError as e:
                    print("Key error")

            return HttpResponseRedirect(reverse("index"))
        else:
            #helper = ArticleFormSetHelper()
            #helper.add_input(Submit("submit","Save"))
            print("Napacni vnosi!")

            #helper.template = "bootstrap/table_inline_formset.html"
            return render(request, "lab/articles.html", {"formset": formset})
                                                                #"helper" : helper})

def shopping_list_helper():
    helper = NakupIzdelkiFormSetHelper()
    helper.template = "bootstrap/table_inline_formset.html"
    return helper

class CreateShoppingView(View):
    def get(self, request,*args, **kwargs):
        form_master = NakupForm(initial={"trgovina" :"Spar",
                                         "datum_nakupa" : "2015-07-03"})
        form_detail = NakupIzdelkiFormset()
        return render(request,"lab/shopping_list.html",
                      {"form_master" : form_master,
                       "form_detail" : form_detail,
                       "action" : reverse("vnos_nakupa")},
                      )

    def post(self, request, *args, **kwargs):
        form_master = NakupForm(request.POST)
        form_detail =  NakupIzdelkiFormset(request.POST)

        if form_master.is_valid():
            nakup_model = form_master.save()
            print("Glava je shranjen")
            if form_detail.is_valid():
                instances = form_detail.save(commit=False)
                i=1
                for instance in instances:
                    print(i)
                    instance.nakup = nakup_model
                    instance.save()
            else:
                print("Erros occured")
                print(form_detail.errors)
                return render(request,"lab/shopping_list.html",
                    {"form_master" : form_master,
                    "form_detail" : form_detail,
                     "action" : reverse("vnos_nakupa")})

            return HttpResponseRedirect(reverse("zgodovina_nakupov"))
        else:
            print("Erros occured")
            return render(request,"lab/shopping_list.html",
              {"form_master" : form_master,
               "form_detail" : form_detail,
                "action" : reverse("vnos_nakupa")})


class EditShoppingView(View):
    def get(self, request,nakup_id, *args, **kwargs):
        nakup = get_object_or_404(Nakup,pk=nakup_id)
        form_master = NakupForm(instance = nakup)
        form_detail = NakupIzdelkiFormset(instance=nakup)
        return render(request,"lab/shopping_list.html",
                      {"form_master" : form_master,
                       "form_detail" : form_detail,
                       "action" : reverse("nakup",
                                          kwargs={"nakup_id":nakup.id})})

    def post(self, request,nakup_id, *args, **kwargs):
        nakup = get_object_or_404(Nakup,pk=nakup_id)
        form_master = NakupForm(request.POST, instance=nakup)
        form_detail =  NakupIzdelkiFormset(request.POST, instance=nakup)

        if form_master.is_valid():
            nakup_model = form_master.save()
            if form_detail.is_valid():
                instances = form_detail.save(commit=False)
                i=1
                for instance in instances:
                    print(i)
                    instance.nakup = nakup_model
                    instance.save()
            else:
                print("Erros occured")
                print(form_detail.errors)
                return render(request,"lab/shopping_list.html",
                      {"form_master" : form_master,
                       "form_detail" : form_detail,
                       "action" : reverse("nakup",
                                          kwargs={"nakup_id":nakup.id})})

            return HttpResponseRedirect(reverse("zgodovina_nakupov"))
        else:
            print("Erros occured")
            return render(request,"lab/shopping_list.html",
                  {"form_master" : form_master,
                   "form_detail" : form_detail,
                   "action" : reverse("nakup",
                          kwargs={"nakup_id":nakup.id})})



class ThanksView(TemplateView):
    template_name = "lab/hvala_za_nakup.html"


class ShoppingHistory(ListView):
    model = Nakup
    template_name = "lab/shopping_history.html"
    context_object_name = "shopping_history"

def test_ajax(request):
    return render(request,"lab/ajax.html")

def ajax_request(request):
    if request.method == "GET":
        try:
            slovene = request.GET["slovene"]
            deutsch = slovene_deutsch[slovene]
        except KeyError as e:
            deutsch=""

        data={"deutsch" : deutsch}
        print(data)
        return JsonResponse(data)
