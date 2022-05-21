from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('prijava', auth_views.LoginView.as_view(template_name='pages/prijava.html'), name ='prijava'),
    path('odjava', auth_views.LogoutView.as_view(template_name='pages/odjava.html'), name ='odjava'),
    path('gost', views.gost, name = 'gost'),
    path('izbor-rezima', views.select_game, name = 'izbor-rezima'),
    path('trening-izbor-tezine', views.tezina_reci, name = 'trening-izbor-tezine'),
    path('kreiraj-lobi', views.kreiraj_lobi, name='kreiraj-lobi'),
    path('upravljanje-admin', views.upravljanje_admin, name='upravljanje-admin'),
    path('izbor-lobija', views.izbor_lobija, name='izbor-lobija'),
]