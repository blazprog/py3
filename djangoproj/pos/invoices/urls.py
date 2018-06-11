from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (index, ArtikelUpdateView, ArtikelListView,ArtikelCreateView,
    SkupinaArtiklaListView, SkupinaArtiklaCreateView,SkupinaArtiklaUpdateView, 
    StrankaCreateView, StrankaUpdateView, StrankaListView, StrankaDeleteView,
    RacunCreateView,PotrditevVnosaRacuna,RacunUpdateView, SeznamRacunov,
    AjaxView,GridView,like_click, suggest_names, get_artikel_details, get_stranka_details,
    get_tabular_template)
from . import views

urlpatterns = patterns("",
   url(r"^$",index, name="index"),
   url(r"^seznam_artiklov$",ArtikelListView.as_view(), name="seznam_artiklov"),
   url(r"^seznam_artiklov/(?P<skupina>\d+)$",ArtikelListView.as_view(), name="seznam_artiklov_filter"),
   url(r"^seznam_skupin_artiklov$",SkupinaArtiklaListView.as_view(), name="seznam_skupin_artiklov"),
   url(r"^seznam_strank/$",StrankaListView.as_view(), name="seznam_strank"),
   url(r"^seznam_racunov/$",SeznamRacunov.as_view(), name="seznam_racunov"),
   url(r"^artikel_edit/(?P<pk>\d+)$",ArtikelUpdateView.as_view(), name="artikel_edit"),
   url(r"^artikel_add$",ArtikelCreateView.as_view(), name="artikel_add"),
   url(r"^stranka_edit/(?P<pk>\d+)$",StrankaUpdateView.as_view(), name="stranka_edit"),
   url(r"^stranka_add$",StrankaCreateView.as_view(), name="stranka_add"),
   url(r"^stranka_delete/(?P<pk>\d+)/$",StrankaDeleteView.as_view(), name="stranka_delete"),
   url(r"^skupina_artikla_edit/(?P<pk>\d+)$",SkupinaArtiklaUpdateView.as_view(), name="skupina_artikla_edit"),
   url(r"^skupina_artikla_add$",SkupinaArtiklaCreateView.as_view(), name="skupina_artikla_add"),
   url(r"^ajax",AjaxView.as_view(), name="ajax"),
   url(r"^grid",GridView.as_view(), name="grid"),
   url(r"^like_click/$",like_click, name="like_click"),
   url(r"^lookup_names/$",suggest_names, name="lookup_names"),
   url(r"^artikel_details/$",get_artikel_details, name="artikel_details"),
   url(r"^stranka_details/$",get_stranka_details, name="stranka_details"),
   url(r"^racun_add/$",RacunCreateView.as_view(), name="racun_add"),
   url(r"^racun_edit/(?P<pk>\d+)$",RacunUpdateView.as_view(), name="racun_edit"),
   url(r"^racun_view/(?P<pk>\d+)$",PotrditevVnosaRacuna.as_view(), name="racun_view"),
   url(r"^search/(?P<table>\w+)/$", get_tabular_template, name="search"),
   url(r"^api/stranke/$", views.customer_list, name="api_seznam_strank"),
   url(r"^api/stranke/(?P<sifra>\d+)$", views.customer_details, name="api_stranka_details"),
)

urlpatterns = format_suffix_patterns (urlpatterns)
