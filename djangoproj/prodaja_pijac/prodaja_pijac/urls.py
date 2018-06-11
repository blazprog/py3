from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prodaja_pijac.views.home', name='home'),
    url(r'^sifranti/', include('sifranti.urls')),
    url(r'^dokumenti/', include('dokumenti.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


