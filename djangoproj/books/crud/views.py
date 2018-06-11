from datetime import date, timedelta
from django.views.generic import  TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.decorators import api_view
from .models import Book
from .serializers import BookSerializer


class AdminPage(TemplateView):
    template_name = 'adminPage.html'


    
#@api_view(('GET',))
#def api_root(request, format=None):
#    return Response({
#        'books': reverse('books-list', request=request, format=format),
#    })

    
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

