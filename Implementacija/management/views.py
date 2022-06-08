# Autori: Merisa Harcinovic 0258/19,  Magdalena Cvorovic 0670/19, Mehmed Harcinovic 0261/19
import random
from string import ascii_letters

from django.core import mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from models import models

from django.core.mail import send_mail
from django.conf import settings

def index(request):
    return render(request, 'pages/index.html')

def manual(request):
    return render(request, 'pages/uputstvo.html')

def registration(request):
    """
    # Funkcija kojom se vrsi registracija korisnika
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    """

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
        email : string
        '''
        email = request.POST["email"]
        '''
        korisnickoime : string
        '''
        korisnickoime = request.POST["korisnickoime"]
        '''
        lozinka : string
        '''
        lozinka = request.POST["lozinka"]

        if not korisnickoime or len(models.Korisnik.objects.filter(username=korisnickoime)):
            error_message = "Neispravno korisnicko ime ili vec postoji korisnik sa tim korisnickim imenom"
        elif not email or len(models.Korisnik.objects.filter(email=email)):
            error_message = "Neispravan email ili vec postoji korisnik sa tim email-om"
        elif not lozinka:
            error_message = "Unesite lozinku"
        else:
            '''
            korisnik : Korisnik
            '''
            korisnik= models.Korisnik.objects.create_user(username=korisnickoime, email=email, password=lozinka, tipKorisnika='osnovni')

            if korisnik:
                #kreiranje korisnika u bazi
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
    """
    # Funkcija kojom se kreira lobi preko zadatog imena i tezine reci
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    """

    if request.user.tipkorisnika == models.Korisnik.ADMIN:
        return redirect('index')

    if request.method == 'POST':
        '''
        imeLobija: string
        Ime lobija koji se kreira
        '''

        imeLobija = request.POST["imeLobija"]


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
        #Selektovana rec iz html strane
        rec = request.POST['selectedRec']

        # Rec nije uneta
        if (rec == "Odaberi rec") or len(imeLobija)==0:
            # ponovno renderovanje strane sa porukom
            return render(
                request,
                'pages/kreiraj-lobi.html', {
                    "reci": models.Rec.objects.all(),
                    "error_msg": "Morate uneti sve podatke."
                }
            )
        # rec iz baze
        recbaza = models.Rec.objects.get(rec__iexact=rec)

        #Update lobija i partije sa njenim kreatorom.
        partija = models.Partija.objects.create(idigra=igra, idrec1 = recbaza, idkor1 = request.user)
        partija.save()
        lobi = models.Lobi.objects.create(ime=imeLobija, tip=tip, tezina=recbaza.tezina, idkor1=user, idpartija = partija)
        lobi.save()

        #Prelazak na igru
        return redirect(f"/game/{partija.idigra_id}")

    return render(
        request,
        'pages/kreiraj-lobi.html',{
            "reci":models.Rec.objects.all(),
        }
    )

@login_required(login_url='prijava')
def rang_lista(request):
    """
    # Funkcija kojom se kreira rang lista igraca
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    """
    '''
        order_by: string
    '''
    order_by = request.GET.get('order_by', '-brojpobeda')
    '''
        users: Igrac
    '''
    users = models.Igrac.objects.all().order_by(order_by)


    return render(
        request,
        'pages/rang-lista.html',
        {
            "users": users,
            
        }
    )



@login_required(login_url='prijava')
def izbor_lobija(request):
    """
    # Funkcija kojom se vrsi izbor lobija
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    """
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
    """
    # Funkcija kojom se vrsi odjava sa sistema
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    """
    logout(request)
    # Redirect to a success page.
    return render(request, 'pages/odjava.html')


def gost(request):
    """
    # Funkcija kojom se korisnik prijavljuje na sistem kao Gost
       :param request: WSGIRequest
       :return: HttpResponse: Renderovana html stranica
    """

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

        ime = request.POST["gostime"]
        if not ime:
            error_message = "Unesite ime"
        else:
            ime = ime + '_' + ''.join(random.choice(ascii_letters) for i in range(4))
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
    """
    # Funkcija kojom se vrsi izbor rezima igre - Trening ili Multiplayer
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    """
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
    """
   # Funkcija kojom se vrsi izbor tezine reci - Lako, Srednje ili Tesko
       :param request: WSGIRequest
       :return: HttpResponse: Renderovana html stranica
   """
   
    '''
    error_message: string
    '''
    error_message = None
    if request.method == 'POST':
        '''
        tezina: string
        '''
        tezina = request.POST['checks[]']

        if tezina!=None:
            if request.user.username:
                return redirect(f"trening/{tezina}/{request.user.username}")
            elif request.session['gost']:
                return redirect(f"trening/{tezina}/{request.session['gost']}")
            else:
                return redirect(f"trening/{tezina}/{''.join(random.choice(ascii_letters) for i in range(4))}")
    return render(
        request,
        'pages/trening-izbor-tezine.html',
        {
            "error_message": error_message,
            
        }
    )


def reset_password(request):
    """
    # Funkcija kojom se vrsi resetovanje loznike
        :param request: WSGIRequest
        :return: HttpResponse: Renderovana html stranica
    """
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
        email: string
        '''
        email = request.POST["email"]

        if not email:
            error_message = "Unesite email"
        else:
            if models.Korisnik.objects.postoji_korisnik_email(email):
                '''
                password: string
                '''
                password = models.Korisnik.objects.make_random_password()
                '''
                subject: string
                '''
                subject = 'Cik Pogodi | Resetovanje lozinke'
                '''
                message: string
                '''
                message = 'Postovani, \n Vasa nova lozinka je %s.' % password
                '''
                email_from: string
                '''
                email_from = settings.EMAIL_HOST_USER
                '''
                recipient_list: list of strings
                '''
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)
                '''
                korisnik: Korisnik
                '''
                korisnik = models.Korisnik.objects.filter(email=email)[0]
                #azuriranje nove lozinke u bazi
                korisnik.set_password(password)
                korisnik.save()
                success_message = "Uskoro cete dobiti email sa novom lozinkom."
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


@login_required(login_url='prijava')
def pridruzi_se_lobiju(request, idlobi):

    """
    #Funkcija koja vraca formu za pridruzivanje lobiju
    :param request: request
    :param idlobi: idlobija kojem pokusavamo da se pridruzimo
    :return:
    """

    if request.user.tipkorisnika==models.Korisnik.ADMIN:
        return redirect('index')

    with transaction.atomic():
        error_message = None
        success_message = None
        context = {
            "error_message": error_message,
            "success_message": success_message
        }
        #Lobi kojem pokusavamo da se pridruzimo
        lobi =get_object_or_404(models.Lobi, idpartija=idlobi)

        #scenario ako je korisnik koji trazi pridruzivanje lobiju vec u tom lobiju. Prosledjuje ga direktno na igru
        if (lobi.idkor1 == request.user or lobi.idkor2 ==request.user):
            return redirect(f"/game/{lobi.idpartija.idigra_id}")
        #scenario da je lobi pun.
        if (lobi.idkor1 and lobi.idkor2) or lobi.status == models.Lobi.U_TOKU:
            return redirect('izbor-lobija')



        if request.method == 'POST':
            #obelezena rec
            rec = request.POST['selectedRec']

            #Rec nije uneta
            if(rec == "Odaberi rec"):
                #ponovno renderovanje strane sa porukom
                return render(
                    request,
                    'pages/pridruzi-se-lobiju.html', {
                        "lobi": lobi,
                        "reci": models.Rec.objects.filter(tezina=lobi.tezina),
                        "error_msg": "Niste uneli rec."
                    }
                )
            #rec iz baze
            recbaza = models.Rec.objects.get(rec__iexact=rec)
            with transaction.atomic():
                #Update partija sa novim protivnikom i novom reci.
                partija = models.Partija.objects.get(idigra = lobi.idpartija.idigra)
                if partija.idkor2 or partija.idrec2:
                    return redirect('izbor-lobija')
                partija.idrec2 = recbaza
                partija.idkor2 = request.user
                lobi.idkor2 = request.user
                lobi.status = models.Lobi.U_TOKU
                lobi.save()
                partija.save()
                #prelazak na igru
                return redirect(f"/game/{partija.idigra_id}")


        return render(
            request,
            'pages/pridruzi-se-lobiju.html', {
                "lobi":lobi,
                "reci":models.Rec.objects.filter(tezina=lobi.tezina)
            }
        )



# def upravljanje_admin(request):
#     success_message = None
#     error_message = None
#
#     return render(
#         request,
#         'management/korisnici-admin.html',
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
#             #     'management/prijava.html',
#             #     {
#             #         "error_message": error_message,
#             #         "success_message": success_message
#             #     }
#             # )