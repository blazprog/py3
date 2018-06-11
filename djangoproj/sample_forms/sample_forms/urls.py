from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sample_forms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^books/', include('books.urls')),
    url(r'^words/', include('words.urls', namespace="words")),
    url(r'^recipes/', include('recipes.urls', namespace="recipes")),
    url(r'^pictures/', include('slike.urls', namespace="pictures")),

)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
                            (r"media/(?P<path>.*)",
                             "serve",
                             {"document_root": settings.MEDIA_ROOT}), )
