from django.conf.urls import patterns, url
from  slike import views


urlpatterns = patterns('',
    url(r'^add_picture$', views.add_picture, name='add_picture'),
    url(r'^list_pictures$', views.list_pictures, name='list_pictures'),
)
