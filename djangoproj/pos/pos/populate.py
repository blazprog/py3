__author__ = 'blazko'
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos.settings')

import django
django.setup()

from invoices.models import Artikel


def populate():
    artikli = (
        ('jeruz','Jeruzalemčab','dcl',0.9),
        ('jabso','Jabolčni sok','dcl',1.2),
        ('juice','Juice','dcl',1.3),
        ('zganj','Žganje','cl',2.1),
        ('balan','Whiskey Balan.','cl',2.7),
        ('kavak','Kava','kos',1),
        ('kavad','Kava podaljšana','kos',1.1),
        ('kavam','Kava z mlekom','kos',1.2),
        ('cajsa','Čaj sadni','kos',1.5),
        ('cajze','Čaj zelen','kos',1.5),
    )

    for artikel in artikli:
        artikel_obj = Artikel(sifra =artikel[0],
                   naziv = artikel[1],
                   em = artikel[2], cena=artikel[3])
        print(artikel_obj)
        artikel_obj.save()

populate()