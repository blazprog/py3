from django.conf.urls import patterns, url
from  books import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^add_book$', views.add_book, name='add_book'),
    url(r'^thanks$', views.thanks, name='thanks'),
)