import random
from string import ascii_letters

from django.core import mail
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required

from accounts import models

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
        'pages/kreiraj-lobi.html',
        {
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
        'pages/izbor-rezima.html',
        {
            "error_message": error_message,
            "success_message": success_message
        }
    )
