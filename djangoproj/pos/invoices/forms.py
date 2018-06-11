__author__ = 'blazko'
from django import forms
from django.forms.models import formset_factory, inlineformset_factory, BaseInlineFormSet

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field,Div,Fieldset,HTML, Button
from crispy_forms.bootstrap import FormActions
from django.core.urlresolvers import reverse

from django.forms import ModelForm, CharField, TextInput, HiddenInput, Form,ChoiceField
from .models import Artikel, SkupinaArtikla, Stranka, Racun, RacunPozicija


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



class RacunForm(ModelForm):
    txtSifraStranke = forms.CharField(label='Sifra stranke',max_length=10)
    txtNazivStranke = forms.CharField(label='Naziv stranke', max_length=50)
    class Meta:
        model = Racun
        fields = ['stevilka','stranka','datum_izdaje',
                'kraj_izdaje',
                'datum_valute',
                 'datum_storitve',
                 'prodajalec',
                 'prodajni_pogoji',
                 'referenca']
        #Ce pustim default select, bo downloadal vse stranke
        widgets = {"stranka" : HiddenInput(),
                   "stevilka": HiddenInput()}

    helper = FormHelper()
    helper.form_method = "post"
    helper.form_class = "form-horizontal"
    helper.label_class = "col-xs-4"
    helper.field_class = "col-xs-8"
    helper.layout = Layout (
            Div(
                Div('stevilka','stranka',
                    'txtSifraStranke','txtNazivStranke',
                    Field('datum_izdaje',css_class='input-sm'),'kraj_izdaje','datum_valute',css_class='col-xs-6'),
                Div('datum_storitve','prodajalec','prodajni_pogoji','referenca',css_class='col-xs-6'),
                css_class='row-fluid form-group-sm',
                )
    )
    helper.form_tag = False

class RacunPozicijaForm(ModelForm):
    class Meta:
        model = RacunPozicija
        fields = ['artikel','txtSifraArtikla','txtNazivArtikla', 
            'kolicina', 'cena', 'davek', 'popust']
        widgets = {"artikel" : TextInput(),
                'txtSifraArtikla':TextInput(attrs={'class':'input-sifraArtikla'})}

    def skupaj(self):
        return self.instance.kolicina * self.instance.cena * (100-self.instance.popust)/100 * (100+self.instance.davek)/100
    

class RacunPozicijaInlineFormset(BaseInlineFormSet):
    def clean(self):
        #Za enkrat se ne rabim
        super().clean()


RacunPozicijaFormset = inlineformset_factory(Racun,RacunPozicija, 
        form=RacunPozicijaForm,
        formset=RacunPozicijaInlineFormset,
        extra=3)

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


