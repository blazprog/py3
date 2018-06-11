from django.db import models

class Avto(models.Model):
    znamka = models.CharField(max_length=30)


a = Avto(znamka="Fiat")
print(Avto.objects.all())


