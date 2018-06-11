__author__ = 'blazko'

from django.conf.urls import include, url
from .views import (index, NameView, ContactMeView, EditArticlesView, test_ajax, ajax_request,
       CreateShoppingView,ThanksView, ShoppingHistory, EditShoppingView)

urlpatterns = [
       url(r"^$",index, name="index"),
       url(r"^enter_name$",NameView.as_view(), name="enter_name"),
       url(r"^contact_me$",ContactMeView.as_view(), name="contact_me"),
       url(r"^articles$",EditArticlesView.as_view(), name="articles"),
       url(r"^test_ajax$",test_ajax, name="test_ajax"),
       url(r"^ajax_request/$",ajax_request, name="ajax_request"),
       url(r"^vnos_nakupa/$",CreateShoppingView.as_view(), name="vnos_nakupa"),
       url(r"^hvala/$",ThanksView.as_view(), name="hvala"),
       url(r"^zgodovina_nakupov/$",ShoppingHistory.as_view(), name="zgodovina_nakupov"),
       url(r"^nakup/(?P<nakup_id>\d+)/$",EditShoppingView.as_view(), name="nakup"),

       ]

