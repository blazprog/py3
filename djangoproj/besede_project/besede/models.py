from django.db import models

class TujaBeseda(models.Model):
    beseda = models.CharField(max_length=120)
    opis = models.TextField()
    uporaba = models.TextField()
    prevod = models.CharField(max_length=120)

