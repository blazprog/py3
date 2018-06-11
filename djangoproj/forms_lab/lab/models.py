from django.db import models

class Nakup(models.Model):
    datum_nakupa = models.DateField()
    trgovina = models.CharField(max_length=30)


class NakupIzdelki(models.Model):
    nakup = models.ForeignKey(Nakup)
    izdelek = models.CharField(max_length=30)
    kolicina = models.IntegerField(default=1)
    cena = models.FloatField(default=0)







