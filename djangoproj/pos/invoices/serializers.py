from .models import Stranka
from rest_framework import serializers


class StrankaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stranka
        fields = ('id','sifra', 'naziv','ulica', 'kraj')
                
