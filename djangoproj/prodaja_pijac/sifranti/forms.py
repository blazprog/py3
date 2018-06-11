__author__ = 'blazko'
from django import forms
from django.forms.models import formset_factory, inlineformset_factory, BaseInlineFormSet
from django.core.urlresolvers import reverse
from django.forms import ModelForm, CharField, TextInput, HiddenInput, Form,ChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field,Div,Fieldset,HTML, Button
from crispy_forms.bootstrap import FormActions

from .models import Artikel, SkupinaArtikla, Stranka


class ArtikelForm(ModelForm):
    class Meta:
        model =  Artikel
        fields = ["sifra","naziv","skupina","em","cena",'davek']
        labels = {"sifra" : "Šifra",
                  "naziv" : "Naziv",
                  "skupina" : "Skupina",
                  "em" : "Em",
                  "cena" : "Cena",
                  "davek" : "Davek"}

    helper = FormHelper()
    helper.form_method = "post"
    helper.form_class = "form-horizontal" #Ker imam form_tag False
                                               # moram class="form-horizontal"
                                               # napisati tudi v templateu
    helper.label_class = "col-md-1"
    helper.field_class = "col-md-4"
    helper.layout = Layout (
        Fieldset("Vnos artikla","sifra", "naziv", "skupina","em", "cena",'davek'),
        FormActions(Submit("save", "Save changes"),
                    HTML('<a class="btn btn-default" href={% url "seznam_artiklov" %}>Cancel</a>'),
                    )
    )
    helper.form_tag = False




class SkupinaArtiklaForm(ModelForm):
    class Meta:
        model = SkupinaArtikla
        fields = ["naziv"]
        labels = {"naziv" : "Naziv skupine"}

    helper = FormHelper()
    helper.form_method = "post"
    helper.form_class = "form-horizontal"
    helper.label_class = "col-lg-1"
    helper.field_class = "col-lg-4"
    helper.layout = Layout (
        Fieldset("Vnos skupine artikla","naziv"),
        FormActions(Submit("save", "Save changes"),
                    Button("cancel","Cancel", css_class="btn btn-default")
                    )
    )
    helper.form_tag = False




class StrankaForm(ModelForm):

    class Meta:
        model =  Stranka
        fields = ["sifra","naziv","posta","ulica","kraj"]
        labels = {"sifra" : "Šifra",
                  "naziv" : "Naziv",
                  "posta" : "Pošta]",
                  "ulica" : "Ulica",
                  "kraj" : "Kraj"}

    helper = FormHelper()
    helper.form_method = "post"
    helper.form_class = "form-horizontal" #Ker imam form_tag False
                                               # moram class="form-horizontal"
                                               # napisati tudi v templateu
    helper.label_class = "col-md-1"
    helper.field_class = "col-md-4"
    helper.layout = Layout (
        Fieldset("Vnos stranke","sifra", "naziv", "posta", "ulica","kraj"),
        FormActions(Submit("save", "Save changes"),
                    HTML('<a class="btn btn-default" href={% url "seznam_strank" %}>Cancel</a>'),
                    )
    )
    helper.form_tag = False

