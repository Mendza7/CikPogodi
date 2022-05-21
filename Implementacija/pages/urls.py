from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uputstvo', views.manual, name='uputstvo'),
    path('registracija', views.registration, name='registracija'),
    path('reset-lozinke', views.reset_password, name='reset-lozinke'),
    path('trening-izbor-tezine', views.tezina_reci, name = 'trening-izbor-tezine'),
    path('rang-lista', views.rang_lista, name='rang-lista'),


]