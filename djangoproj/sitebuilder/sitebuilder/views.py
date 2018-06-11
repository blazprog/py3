import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.template import Template
from django.utils._os import safe_join


def get_page_or_404(name):
    """Return page content as django template or raise 404 error"""

    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY,name)
    except ValueError:
        raise Http404('Page not found')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page not found')

    with open(file_path,'r') as f:
        page = Template(f.read() )

    return page


def page(request, slug='index'):
    file_name ='{}.html'.format(slug)
    page = get_page_or_404(file_name)
    context = {
        'slug': slug,
        'page': page,
    }
    return render(request, 'page.html', context)
