from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from snippets import views


router = DefaultRouter()
router.register(r'snippets',views.SnippetViewSet)
router.register(r'users',views.UserViewSet)

urlpatterns = [
            url(r'^', include(router.urls)),
        ]

#urlpatterns = [
#    url(r'^snippets/$', views.SnippetList.as_view(),name='snippet-list'),
#    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(),
#        name='snippet-detail'),
#    url(r'^users/$', views.UserList.as_view(),name='user-list'),
#    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(),
#        name='user-detail'),
#    url(r'^$', views.api_root),
#    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', 
#            views.SnippetHighlight.as_view(), name='snippet-highlight'),
#]
#
#urlpatterns = format_suffix_patterns(urlpatterns)
