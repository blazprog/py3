from django.contrib import admin
from .models import VrstaArtikla, Artikel, Em, DDV, Stranka, Posta, Drzava

admin.site.register(VrstaArtikla)
admin.site.register(Em)
admin.site.register(Artikel)
admin.site.register(DDV)
admin.site.register(Stranka)
admin.site.register(Posta)
admin.site.register(Drzava)


