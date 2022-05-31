from random import randint

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from accounts.models import Rec


def Trening(request):
    pass



def trening_id(request, trening_id):
    context = {}

    count = Rec.objects.aggregate(count=Count('idrec'))['count']
    random_ind = randint(0, count - 1)
    rec = Rec.objects.all()[random_ind]
    context['recrec'] = rec.rec
    context['trening_id'] = trening_id

    return render(request, 'trening/trening.html', context)