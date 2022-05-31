import random
from string import ascii_letters

from django.core import mail
from django.shortcuts import render,redirect
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

def kreiraj_lobi(request):
    success_message = None
    error_message = None

    if request.method == 'POST':

        imeLobija = request.POST["imeLobija"]
        lako = request.POST["lako"]
        srednje = request.POST["srednje"]
        tesko = request.POST["tesko"]

        #TODO: kreiraj lobi u bazi

        lobi = models.Lobi.objects.create()

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

def upravljanje_admin(request):
    success_message = None
    error_message = None

    return render(
        request,
        'pages/korisnici-admin.html',
        {
            "error_message": error_message,
            "success_message": success_message
        }
    )

def izbor_lobija(request):
    success_message = None
    error_message = None

    return render(
        request,
        'pages/izbor-lobija.html',
        {
            "error_message": error_message,
            "success_message": success_message
        }
    )


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'pages/odjava.html')


def gost(request):
    success_message = None
    error_message = None

    if request.method == 'POST':

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
    success_message = None
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
