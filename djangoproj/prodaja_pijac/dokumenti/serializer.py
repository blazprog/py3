from rest_framework import serializers
from sifranti.models import Stranka, Artikel
class StrankaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stranka
        fields = ('id','sifra','naziv','posta','ulica','kraj')

class ArtikelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artikel
        fields = ('sifra', 'naziv', 'skupina', 'cena', 'davek', 'em')
