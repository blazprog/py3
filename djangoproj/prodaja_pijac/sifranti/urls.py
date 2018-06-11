from django.conf.urls import patterns, include, url
from .views import (index,ArtikelListView, ArtikelUpdateView, ArtikelCreateView,StrankaListView,StrankaCreateView,
        StrankaUpdateView, StrankaDeleteView,SkupinaArtiklaListView, SkupinaArtiklaCreateView, 
        SkupinaArtiklaUpdateView, ArtikelDeleteView, SkupinaArtiklaDeleteView)

urlpatterns = patterns("",
   url(r"^$",index, name="index"),
   url(r"^seznam_artiklov$",ArtikelListView.as_view(), name="seznam_artiklov"),
   url(r"^seznam_artiklov/(?P<skupina>\d+)$",ArtikelListView.as_view(), name="seznam_artiklov_filter"),
   url(r"^artikel_edit/(?P<pk>\d+)$",ArtikelUpdateView.as_view(), name="artikel_edit"),
   url(r"^artikel_add$",ArtikelCreateView.as_view(), name="artikel_add"),
   url(r"^seznam_strank/$",StrankaListView.as_view(), name="seznam_strank"),
   url(r"^artikel_delete/(?P<pk>\d+)/$",ArtikelDeleteView.as_view(), name="artikel_delete"),
   url(r"^stranka_edit/(?P<pk>\d+)$",StrankaUpdateView.as_view(), name="stranka_edit"),
   url(r"^stranka_add$",StrankaCreateView.as_view(), name="stranka_add"),
   url(r"^stranka_delete/(?P<pk>\d+)/$",StrankaDeleteView.as_view(), name="stranka_delete"),
   url(r"^seznam_skupin_artiklov$",SkupinaArtiklaListView.as_view(), name="seznam_skupin_artiklov"),
   url(r"^skupina_artikla_edit/(?P<pk>\d+)$",SkupinaArtiklaUpdateView.as_view(), name="skupina_artikla_edit"),
   url(r"^skupina_artikla_add$",SkupinaArtiklaCreateView.as_view(), name="skupina_artikla_add"),
   url(r"^skupina_artikla_delete/(?P<pk>\d+)/$",SkupinaArtiklaDeleteView.as_view(), name="skupina_artikla_delete"),
)


