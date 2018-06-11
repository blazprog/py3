from django.db import models

class VrstaArtikla(models.Model):
    naziv = models.CharField(max_length=60)

    def __str__(self):
        return self.naziv

class Em(models.Model):
    naziv = models.CharField(max_length=60)

    def __str__(self):
        return self.naziv

class DDV(models.Model):
    stopnja = models.FloatField(default=0)
    naziv = models.CharField(max_length= 5)
    dolgiNaziv = models.CharField(max_length=20)

    def __str__(self):
        return (
            "{0} - {1}".format(self.stopnja, self.dolgiNaziv)
        )

class Posta(models.Model):
    postnaStevilka = models.CharField(max_length=20)
    naziv = models.CharField(max_length=60)

    def __str__(self):
        return self.naziv + ' ' + self.postnaStevilka

class Drzava(models.Model):
    oznaka = models.CharField(max_length=5)
    naziv = models.CharField(max_length=60)

    def __str__(self):
        return self.naziv

class Artikel(models.Model):
    idVrstaArtikla = models.ForeignKey(VrstaArtikla)
    idEm = models.ForeignKey(Em)
    idDDV = models.ForeignKey(DDV)
    nazivArtikla = models.CharField(max_length=100)
    cena = models.FloatField(default=0)
    dolgiOpis = models.TextField()
    slika = models.ImageField(blank=True,null=True)

    def __str__(self):
        return self.nazivArtikla

class Stranka(models.Model):
    nazivStranke = models.CharField(max_length=60)
    idPosta = models.ForeignKey(Posta)
    idDrzava = models.ForeignKey(Drzava)
    ulica = models.CharField(max_length=60)
    kraj = models.CharField(max_length=60)

    def __str__(self):
        return self.nazivStranke


class Racun(models.Model):
    stevilkaRacuna = models.IntegerField(default=0)
    datumRacuna = models.DateField(auto_now_add=True)
    krajIzdaje = models.CharField(max_length=60)
    sifraStranke = models.ForeignKey(Stranka)


class RacunPostavka(models.Model):
    idRacuna = models.ForeignKey(Racun)
    stevilkaPostavke = models.IntegerField(default=0)
    sifraArtikla = models.ForeignKey(Artikel)
    kolicina = models.FloatField()
    cena = models.FloatField()
    popust = models.FloatField()
    idEm = models.ForeignKey(Em)
    idDDV = models.ForeignKey(DDV)







