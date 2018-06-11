__author__ = 'blazko'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prodaja_pijac.settings')

import django
django.setup()

from sifranti.models import Artikel, SkupinaArtikla


def populate():

    skupine = (
        (1,'Vina'),
        (2,'Brezalkoholne pijače'),
        (3,'Žgane pijače'),
        (4,'Topli napitki'),
        (5,'Piva'),
    )

    artikli = (
        #('jeruz','Jeruzalemčab','dcl',0.9,22,SkupinaArtikla.objects.get(id=1)),
        ('jabso','Jabolčni sok','dcl',1.2,8.5,SkupinaArtikla.objects.get(id=2)),
        ('juice','Juice','dcl',1.3,8.5,SkupinaArtikla.objects.get(id=2)),
        ('zganj','Žganje','cl',2.1,22,SkupinaArtikla.objects.get(id=3)),
        ('balan','Whiskey Balan.','cl',2.7,22,SkupinaArtikla.objects.get(id=3)),
        ('kavak','Kava','kos',1,22,SkupinaArtikla.objects.get(id=4)),
        ('kavad','Kava podaljšana','kos',1.1,22,SkupinaArtikla.objects.get(id=4)),
        ('kavam','Kava z mlekom','kos',1.2,22,SkupinaArtikla.objects.get(id=4)),
        ('cajsa','Čaj sadni','kos',1.5,22,SkupinaArtikla.objects.get(id=4)),
        ('cajze','Čaj zelen','kos',1.5,22,SkupinaArtikla.objects.get(id=4)),
    )

    #for skupina in skupine:
    #    skupina_obj = SkupinaArtikla(naziv = skupina[1])  #id doda django sam
    #    print(skupina_obj)
    #    skupina_obj.save()

    for artikel in artikli:
        artikel_obj = Artikel(sifra =artikel[0],
                   naziv = artikel[1],
                   em = artikel[2], 
                   cena=artikel[3],
                   davek = artikel[4],
                   skupina = artikel[5])
        print(artikel_obj)
        artikel_obj.save()

populate()
