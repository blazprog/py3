from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'vaje_forms.views.home', name='home'),
    url(r'^exercises/select_language$', 'vaje_forms.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grammar/', include("myforms.urls")),
)
