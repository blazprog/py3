from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter
import crud.views 
    

router = DefaultRouter()
router.register(r'books', crud.views.BookViewSet)

urlpatterns = patterns("",
   url(r"^$",crud.views.AdminPage.as_view(), name="adminPage"),
   url(r'^api/', include(router.urls)),
)




