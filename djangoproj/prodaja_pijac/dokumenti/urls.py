from django.conf.urls import patterns, include, url

from .views import (racuni,RacunCreateView, RacunUpdateView, PotrditevVnosaRacuna, 
    get_tabular_template,SeznamRacunov,SeznamDokumentov,TodoExercise,
    suggest_names, get_artikel_details, get_stranka_details,get_artikel_by_id,get_skupina_artiklov,
    StrankeList, StrankaDetail, ArtikelList, ArtikelDetail)        
    

urlpatterns = patterns("",
   url(r"^$",racuni, name="racuni"),
   url(r"^seznam_racunov/$",SeznamRacunov.as_view(), name="seznam_racunov"),
   url(r"^racun_add/$",RacunCreateView.as_view(), name="racun_add"),
   url(r"^racun_edit/(?P<pk>\d+)$",RacunUpdateView.as_view(), name="racun_edit"),
   url(r"^racun_view/(?P<pk>\d+)$",PotrditevVnosaRacuna.as_view(), name="racun_view"),
   url(r"^search/(?P<table>\w+)/$", get_tabular_template, name="search"),
   url(r"^lookup_names/$",suggest_names, name="lookup_names"),
   url(r"^artikel_details/$",get_artikel_details, name="artikel_details"),
   url(r"^get_artikel_by_id/$",get_artikel_by_id, name="get_artikel_by_id"),
   url(r"^get_skupina_artiklov/$",get_skupina_artiklov, name="get_skupina_artiklov"),
   url(r"^stranka_details/$",get_stranka_details, name="stranka_details"),
   url(r"^seznam_dokumentov/$",SeznamDokumentov.as_view(), name="seznam_dokumentov"),
   url(r"^todo/$",TodoExercise.as_view(), name="todo"),
   url(r"^api/stranke/$",StrankeList.as_view(), name="stranke"),
   url(r"^api/stranke/(?P<pk>\d+)$",StrankaDetail.as_view(), name="stranka"),
   url(r"^api/artikli/$",ArtikelList.as_view(), name="artikli"),
   url(r"^api/artikli/(?P<pk>\d+)$",ArtikelDetail.as_view(), name="artikel"),
)
