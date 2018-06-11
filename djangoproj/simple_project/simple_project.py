import sys
import os
from django.conf import settings


BASE_DIR = os.path.dirname( __file__ )
print(BASE_DIR)
DEBUG = os.environ.get('DEBUG','on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY','{{ secretkey }}' )
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')


settings.configure(
        DEBUG=True,
        SECRET_KEY=SECRET_KEY,
        ALLOWED_HOSTS=ALLOWED_HOSTS,
        ROOT_URLCONF=__name__,

    MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),


    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'rest_framework'
    ),

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR,  'templates'),
    ),
        
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR,  'static'),
    ),

    STATIC_URL = '/static/',

)


#Importiram lahko sele potem, ko imam nastavljene settings
from django.http import HttpResponse
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.views.generic import TemplateView



class Index(TemplateView):
    template_name = 'index.html'


urlpatterns = (
            url(r'^$', Index.as_view()),
        )


application = get_wsgi_application()
if __name__ == '__main__':
    print(BASE_DIR)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

