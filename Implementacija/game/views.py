import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render

# Create your views here.
from accounts.models import *


class Game:
    pass

@login_required(login_url='prijava')
def game_id(request, game_id):
    '''

    :param request:
    :param game_id: id igre
    :return:
    '''

    context={
        "rec1":"cerimidjinica",
        "rec2":"cerimidjinica2",
        "game_id":game_id
    }
    return render(request,'game/game.html',context)


def getWords(request, game_d):
    '''
    Funkcija koja dostavlja reci i korisnike multiplayer rezimu.
    :param request:
    :param game_d: id igre za koju hocemo da dohvatimo reci
    :return:
    '''

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'GET':
            gameid = int(game_d)
            partija = Partija.objects.get(idigra_id=gameid)
            rec1 = Rec.objects.get(idrec=partija.idrec1_id).rec
            rec2=None
            if partija.idrec2:
                rec2 = Rec.objects.get(idrec=partija.idrec2_id).rec
            return JsonResponse({
                'user1':partija.idkor1.username,
                'user2':partija.idkor2.username,
                'rec1':rec1,
                'rec2':rec2,
                'first':partija.first_turn
            })
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        print("invalid req")
        return HttpResponseBadRequest('Invalid request')