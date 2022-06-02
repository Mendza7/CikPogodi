# Autor: Merisa Harcinovic 0258/19
import random
from string import ascii_letters

from django.core import mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from accounts import models

from django.core.mail import send_mail
from django.conf import settings

def index(request):
    return render(request, 'pages/index.html')

def manual(request):
    return render(request, 'pages/uputstvo.html')

def registration(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        email = request.POST["email"]
        korisnickoime = request.POST["korisnickoime"]
        lozinka = request.POST["lozinka"]

        if not korisnickoime or len(models.Korisnik.objects.filter(username=korisnickoime)):
            error_message = "Neispravno korisnicko ime ili vec postoji korisnik sa tim korisnickim imenom"
        elif not email or len(models.Korisnik.objects.filter(email=email)):
            error_message = "Neispravan email ili vec postoji korisnik sa tim email-om"
        elif not lozinka:
            error_message = "Unesite lozinku"
        else:
            korisnik= models.Korisnik.objects.create_user(username=korisnickoime, email=email, password=lozinka, tipKorisnika='osnovni')

            if korisnik:
                models.Igrac.create(korisnik)

                success_message = "Uspesno ste se registrovali na sistem"
            else:
                error_message = "Korisnik sa unetim korisnickim imenom ili email-om vec postoji"

    return render(
        request,
        'pages/registracija.html',
        {
            "error_message": error_message,
            "success_message": success_message
        }
    )


@login_required(login_url='prijava')
def kreiraj_lobi(request):
    '''
    # Funkcija kojom se kreira lobi preko zadatog imena i tezine reci
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    '''

    if request.method == 'POST':
        '''
        imeLobija: string
        Ime lobija koji se kreira
        '''

        imeLobija = request.POST["imeLobija"]
        print(imeLobija)

        '''
        tezina: int 
        Tezina reci koja se zadaje pri kreiranju
        '''

        tezina = int(request.POST['checks[]'])

        #kreiraj lobi u bazi
        '''
        igra: Igra 
        '''
        igra = models.Igra.create_igra(tipIgre=models.Igra.PVP)
        igra.save()
        '''
        user: Korisnik
        '''
        user = models.Korisnik.objects.get(idkor=request.user.idkor)
        '''
        tip: string
        '''
        tip = models.Lobi.OSNOVNI
        if(user.tipkorisnika == models.Korisnik.VIP):
            tip = models.Lobi.VIP
        rec = request.POST['rec']
        recbaza = models.Rec.objects.filter(rec__iexact=rec)
        if len(recbaza):
            recbaza = recbaza[0]
            if recbaza.tezina != tezina:
                print("neadekvatna tezina")
                return render(
                    request,
                    'pages/kreiraj-lobi.html', {}
                )
            else:
                partija = models.Partija.objects.create(idigra=igra, idrec1 = recbaza, idkor1 = request.user)
                partija.save()
                lobi = models.Lobi.objects.create(ime=imeLobija, tip=tip, tezina=tezina, idkor1=user, idpartija = partija)
                lobi.save()
                return redirect(f"/game/{partija.idigra_id}")

    return render(
        request,
        'pages/kreiraj-lobi.html',{}
    )

def rang_lista(request):
    success_message = None
    error_message = None
    order_by = request.GET.get('order_by', '-brojpobeda')
    users = models.Igrac.objects.all().order_by(order_by)



    return render(
        request,
        'pages/rang-lista.html',
        {
            "users": users,
            "error_message": error_message,
            "success_message": success_message
        }
    )



def izbor_lobija(request):
    '''
    # Funkcija kojom se vrsi izbor lobija
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    '''
    '''
    success_message: string
    '''
    success_message = None
    '''
    error_message: string
    '''
    error_message = None

    '''
    VipLobi: QuerySet[Lobi]
    Vip lobiji iz baze
    '''
    VipLobi = models.Lobi.objects.filter(tip = models.Lobi.VIP)
    '''
    KorisnikLobi: QuerySet[Lobi]
    Osnovni lobiji iz baze
    '''
    KorisnikLobi = models.Lobi.objects.filter(tip = models.Lobi.OSNOVNI)

    return render(
        request,
        'pages/izbor-lobija.html',
        {
            "vip":VipLobi,
            "osnovni":KorisnikLobi,
            "error_message": error_message,
            "success_message": success_message
        }
    )


def logout_view(request):
    '''
    # Funkcija kojom se vrsi odjava sa sistema
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    '''
    logout(request)
    # Redirect to a success page.
    return render(request, 'pages/odjava.html')


def gost(request):
    '''
    # Funkcija kojom se korisnik prijavljuje na sistem kao Gost
       :param request: WSGIRequest
       :return: HttpResponse: Renderovana html stranica
    '''

    '''
    success_message: string
    '''
    success_message = None
    '''
    error_message: string
    '''
    error_message = None

    if request.method == 'POST':
        '''
        ime: string
        Ime koje je Gost uneo
        '''

        ime = request.POST["gostime"] + '_' + ''.join(random.choice(ascii_letters) for i in range(4))
        if not ime:
            error_message = "Unesite ime"
        else:
            request.session['gost'] = ime
            return redirect('izbor-rezima')


    return render(
        request,
        'pages/gost.html',
        {
            "error_message": error_message,
            "success_message": success_message
        }
    )

def select_game(request):
    '''
    # Funkcija kojom se vrsi izbor rezima igre - Trening ili Multiplayer
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    '''
    '''
    success_message: string
    '''
    success_message = None
    '''
    error_message: string
    '''
    error_message = None

    return render(
        request,
        'pages/izbor-rezima.html',{}
    )

def tezina_reci(request):
    success_message = None
    error_message = None

    if request.method == 'POST':

        lako = request.POST["lako"]
        srednje = request.POST["srednje"]
        tesko = request.POST["tesko"]

        provera = request.POST.getlist('checks[]')

    return render(
        request,
        'pages/trening-izbor-tezine.html',
        {
            "error_message": error_message,
            "success_message": success_message
        }
    )


def reset_password(request):
    success_message = None
    error_message = None

    if request.method == 'POST':
        email = request.POST["email"]

        if not email:
            error_message = "Unesite email"
        else:
            if models.Korisnik.objects.postoji_korisnik_email(email):

                password = models.Korisnik.objects.make_random_password()
                subject = 'Cik Pogodi | Resetovanje lozinke'
                message = 'Vasa nova lozinka je %s' % password
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)

                korisnik = models.Korisnik.objects.filter(email=email)[0]
                korisnik.set_password(password)
                korisnik.save()
                success_message = "Uskoro cete dobiti email sa novom lozinkom: %s" % password
            else:
                error_message = "Korisnik sa unetim email-om ne postoji"

    return render(
        request,
        'pages/reset-lozinke.html',
        {
            "error_message": error_message,
            "success_message": success_message
        }
    )


def pridruziSeLobiju(request, idlobi):
    with transaction.atomic():
        lobi =get_object_or_404(models.Lobi, idlobi=idlobi)
        if (lobi.idkor1 and lobi.idkor2) or lobi.status == models.Lobi.U_TOKU:
            return redirect('izbor-lobija')

        if request.method == 'POST':

            rec = request.POST['rec']
            recbaza = models.Rec.objects.filter(rec__iexact=rec)
            if len(recbaza):
                recbaza = recbaza[0]
                if recbaza.tezina != lobi.tezina:
                    print("neadekvatna tezina")
                    return render(
                        request,
                        'pages/pridruzi-se-lobiju.html', {}
                    )

                else:
                    partija = models.Partija.objects.get(idigra = lobi.idpartija.idigra)
                    partija.idrec2 = recbaza
                    partija.idkor2 = request.user
                    lobi.idkor2 = request.user
                    lobi.status = models.Lobi.U_TOKU
                    lobi.save()
                    print(lobi)
                    partija.save()
                    return redirect(f"/game/{partija.idigra_id}")
            else:
                print("ne postoji rec")
                return render(
                    request,
                    'pages/pridruzi-se-lobiju.html', {}
                )

        return render(
            request,
            'pages/pridruzi-se-lobiju.html', {}
        )



# def upravljanje_admin(request):
#     success_message = None
#     error_message = None
#
#     return render(
#         request,
#         'pages/korisnici-admin.html',
#         {
#             "error_message": error_message,
#             "success_message": success_message
#         }
#     )


# def login(request):
#     success_message = None
#     error_message = None
#
#     if request.method == 'POST':
#
#         korisnickoime = request.POST["korisnickoime"]
#         lozinka = request.POST["lozinka"]
#
#         korisnik = authenticate(request, username=korisnickoime, password=lozinka)
#
#
#         if korisnik is not None:
#             login(request)
#             success_message = "Uspesno ste se ulogovali na sistem"
#             return redirect('izbor-rezima')
#
#         else:
#             error_message = "Neispravno korisnicko ime ili lozinka"
#             # return render(
#             #     request,
#             #     'pages/prijava.html',
#             #     {
#             #         "error_message": error_message,
#             #         "success_message": success_message
#             #     }
#             # )