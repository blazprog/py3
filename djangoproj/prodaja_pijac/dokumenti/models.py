from django.db import models
from sifranti.models import Stranka, Artikel

class RacunRekapitulacija:
    def __init__(self, racun):
        pozicije = RacunPozicija.objects.filter(racun=racun)
        self.skupniZnesek = 0
        self.skupajBrezDavka = 0
        self.skupajDavki = 0
        self.davki = {}
        for pozicija in pozicije:
            znesek_popust = (pozicija.kolicina * pozicija.cena *
                     (100-pozicija.popust)/100 )

            davek = pozicija.davek
            znesek_davek = znesek_popust * (davek/100)
            if davek in self.davki.keys():
                self.davki[davek] += znesek_davek 
            else:
                self.davki[davek] = znesek_davek

            self.skupajBrezDavka += znesek_popust
            self.skupajDavki += znesek_davek
            self.skupniZnesek += (znesek_popust + znesek_davek)
                

class Racun(models.Model):
    stevilka = models.IntegerField(default=0)
    stranka = models.ForeignKey(Stranka,related_name='sifranti_stranka')
    datum_izdaje = models.DateField()
    kraj_izdaje = models.CharField(max_length=50)
    datum_valute = models.DateField()
    datum_storitve = models.DateField()
    prodajalec = models.CharField(max_length=50)
    prodajni_pogoji = models.CharField(max_length=50)
    referenca = models.CharField(max_length=50)

    def skupniZneski(self):
        return RacunRekapitulacija(self)

    def __str__(self):
        return '{}, {}'.format(self.stevilka, self.stranka)

    

class RacunPozicija(models.Model):
    racun = models.ForeignKey(Racun,related_name='dokumenti_racun')
    zaporedna_stevilka = models.IntegerField()
    artikel = models.ForeignKey(Artikel,related_name='sifranti_artikel')
    txtSifraArtikla = models.CharField(max_length=5)
    txtNazivArtikla = models.CharField(max_length=25)
    kolicina = models.FloatField(default=1)
    cena = models.FloatField(default=0)
    davek = models.FloatField(default=0)
    popust = models.FloatField(default=0)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.racun, self.zaporedna_stevilka, self.artikel,self.kolicina)
    
    def skupaj(self):
        return self.cena * self.kolicina * (100+self.davek)/100 * (100-self.popust)/100

class DocumentCounter(models.Model):
    document = models.CharField(max_length=30)
    next_number = models.IntegerField(default=1)

    def __str__(self):
        return '{} - {}'.format(self.document,self.next_number)

def getNextDocumentNumber(document):
    print(document)
    counter = DocumentCounter.objects.get(document=document)
    print(counter)
    i = counter.next_number
    counter.next_number += 1
    counter.save()
    return i



class Counter(models.Model):
    num_counts=models.IntegerField()

    def __str__(self):
        return "{}, {}".format(self.id, self.num_counts)
