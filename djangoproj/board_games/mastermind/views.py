from random import shuffle

from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


class Index(View):
    def __init__(self):
        pass

    def get(self,request):
        pieces = []
        for i in range (1,7):
            pieces.append('c{0}'.format(i))

        shuffle(pieces) 
        context = {}        
        context['piece1'] = pieces[0]
        context['piece2'] = pieces[1]
        context['piece3'] = pieces[2]
        context['piece4'] = pieces[3]

        return render(request, 'mastermind/mastermind.html', context) 
