from django.conf.urls import patterns, url
from  words import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^add_word$', views.add_word, name='add_word'),
    url(r'^practice$', views.practice_words, name='practice'),
    url(r'^list$', views.list_all_words, name='list'),
    url(r'^check_answer/$', views.check_answer, name='check_answer'),
    url(r'^check_json/$', views.check_json, name='check_json'),
    url(r'^get_singer_details/$', views.get_singer_details, name='get_singer_details'),
)