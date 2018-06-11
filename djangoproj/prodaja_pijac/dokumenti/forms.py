from django import forms
from django.forms.models import formset_factory, inlineformset_factory, BaseInlineFormSet
from django.core.urlresolvers import reverse

from django.forms import ModelForm, CharField, TextInput, HiddenInput, Form,ChoiceField
from sifranti.models import Artikel, SkupinaArtikla, Stranka 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field,Div,Fieldset,HTML, Button
from crispy_forms.bootstrap import FormActions

from .models import Racun, RacunPozicija

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
