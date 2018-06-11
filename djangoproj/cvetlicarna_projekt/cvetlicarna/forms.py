from django.forms import ModelForm, TextInput, Select
from django.forms.models import inlineformset_factory

from .models import Artikel, Stranka, Racun, RacunPostavka

class ArtikelForm(ModelForm):
    class Meta:
        model = Artikel
        fields = ["idVrstaArtikla","idEm",  "idDDV", "nazivArtikla", "cena", "dolgiOpis"]

class StrankaForm(ModelForm):
    class Meta:
        model = Stranka
        fields = ["nazivStranke","idPosta","idDrzava","ulica","kraj"]


class RacunForm(ModelForm):
    class Meta:
        model = Racun
        fields =["stevilkaRacuna", "krajIzdaje", "sifraStranke"]


RacunFormset = inlineformset_factory(Racun, RacunPostavka, fk_name="idRacuna",
                                     fields=["idRacuna","stevilkaPostavke","sifraArtikla",
                                             "kolicina","cena","popust","idEm","idDDV"],
                                     widgets={"kolicina": TextInput(attrs={"class": "kolicina"}),
                                              "sifraArtikla" : Select(attrs={"class":"sifraArtikla"})},
                                     extra=12
                                     )



