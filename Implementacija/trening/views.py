#Autor : Mehmed Harčinović 0261/19
from random import randint

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from models.models import Rec


def Trening(request):
    pass



def trening_id(request,tezina, trening_id):
    """

    :param request:ASGIRequest
    :param tezina: string, zadata tezina
    :param trening_id: string , id treninga
    :return:
    """
    #tezina reci
    tez = int(tezina)
    context = {}
    #odabir random reci iz baze
    count = Rec.objects.filter(tezina=tez).aggregate(count=Count('idrec'))['count']
    random_ind = randint(0, count - 1)
    #odabrana rec
    rec = Rec.objects.filter(tezina=tez)[random_ind]
    context['recrec'] = rec.rec
    context['trening_id'] = trening_id

    return render(request, 'trening/trening.html', context)