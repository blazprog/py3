from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from board.urls import router
#from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'scrum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^api/token/',obtain_auth_token,name='api-token'),
    url(r'^api/',include(router.urls)),
    url(r'^$',TemplateView.as_view(template_name='board/index.html')),
)
