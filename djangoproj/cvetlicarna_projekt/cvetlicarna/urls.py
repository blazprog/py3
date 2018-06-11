from django.conf.urls import patterns, include, url
from . import views
from .views import SeznamArtiklov, SeznamStrank, UpdateArtikelView, UpdateStrankaView,SeznamRacunov

urlpatterns = patterns('',
    url(r'^$', views.index , name='index'),
    url(r'^seznam_artiklov$', SeznamArtiklov.as_view() , name='seznam_artiklov'),
    url(r'^seznam_strank$', SeznamStrank.as_view() , name='seznam_strank'),
    url(r'^seznam_racunov$', SeznamRacunov.as_view() , name='seznam_racunov'),
    url(r'^dodaj_artikel$', views.dodaj_artikel , name='dodaj_artikel'),
    url(r'^uredi_artikel/(?P<pk>\d+)$', UpdateArtikelView.as_view() , name='uredi_artikel'),
    url(r'^dodaj_stranko$', views.dodaj_stranko , name='dodaj_stranko'),
    url(r'^uredi_stranko/(?P<pk>\d+)$', UpdateStrankaView.as_view(), name='uredi_stranko'),
    url(r'^dodaj_racun$', views.dodaj_racun, name='dodaj_racun'),
    url(r'^uredi_racun/(?P<pk>\d+)$', views.uredi_racun, name='uredi_racun'),
    url(r'^get_artikel_details/$', views.get_artikel_details, name='get_artikel_details'),
    # url(r'^blog/', include('blog.urls')),
)