import sys
import os
from io import BytesIO
from PIL import Image, ImageDraw
from django.conf import settings


DEBUG = os.environ.get('DEBUG','on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY','thhisisverysecretkey' )
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')

BASE_DIR = os.path.dirname(__file__)
settings.configure(
        DEBUG=True,
        SECRET_KEY=SECRET_KEY,
        ALLOWED_HOSTS=ALLOWED_HOSTS,
        ROOT_URLCONF=__name__,
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),

        INSTALLED_APPS=(
            'django.contrib.staticfiles', #da lahko v template uporabim {% load staticfiles %}
        ),

        TEMPLATE_DIRS = (
            os.path.join(BASE_DIR, 'templates'),
        ),
        
        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, 'static'),
        ),

        STATIC_URL = '/static/'
    )



#Importiram lahko sele potem, ko imam nastavljene settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf.urls import url
from django import forms
from django.core.wsgi import get_wsgi_application
from django.shortcuts import render
from django.core.urlresolvers import reverse


class ImageForm(forms.Form):
    """Form to validate request placeholder image """

    height = forms.IntegerField(min_value=1, max_value=2000)
    width = forms.IntegerField(min_value=1, max_value=2000)

    def generate(self, image_format='PNG'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        image = Image.new('RGB',(width,height))
        draw = ImageDraw.Draw(image)
        text = '{} x {}'.format(width, height)
        textwidth, textheight = draw.textsize(text)
        #preverim, ce je kvadrat dovolj velik, da imam kak pisati
        if textwidth < width and textheight < height:
            texttop  =(height - textheight) // 2
            textleft = (width - textwidth) // 2
            draw.text((textleft, texttop), text, fill=(55, 155, 155))
        content = BytesIO() #A stream implementation using an in-memory bytes buffer. 
        image.save(content, 'PNG')
        content.seek(0)
        return content  #returns image content as bytes



def placeholder(request, width, height):
    form = ImageForm({'height':height,'width':width})
    if form.is_valid():
        return HttpResponse(form.generate(), content_type='image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Range')


def index(request):
    example = reverse('placeholder', kwargs={'width':50, 'height': 50})
    context = {
        'example': request.build_absolute_uri(example)
    }
    return render(request,'home.html', context)


urlpatterns = (
            url(r'^$', index,name='homepage'),
            url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', 
                    placeholder,name='placeholder'),
        )


application = get_wsgi_application()



if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

