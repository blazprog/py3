from django.conf.urls import patterns, include, url
from .views import IndexView, CarsView, CarsCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
       url(r"^$",IndexView.as_view(), name="index"),
       url(r"cars",CarsView.as_view(), name="cars_gallery"),
       url(r"^upload_car/$",CarsCreateView.as_view(), name="upload_car"),
       #url(r"^contact_me$",ContactMeView.as_view(), name="contact_me"),
       #url(r"^articles$",EditArticlesView.as_view(), name="articles"),
       #url(r"^test_ajax$",test_ajax, name="test_ajax"),
       #url(r"^ajax_request/$",ajax_request, name="ajax_request"),
       #url(r"^vnos_nakupa/$",CreateShoppingView.as_view(), name="vnos_nakupa"),
       #url(r"^hvala/$",ThanksView.as_view(), name="hvala"),
       #url(r"^zgodovina_nakupov/$",ShoppingHistory.as_view(), name="zgodovina_nakupov"),
       #url(r"^nakup/(?P<nakup_id>\d+)/$",EditShoppingView.as_view(), name="nakup"),
       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
