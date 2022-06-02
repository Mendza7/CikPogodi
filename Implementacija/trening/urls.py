#Autor: Mehmed Harcinovic 0261/19
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Trening),
    path('<str:tezina>/<str:trening_id>/',views.trening_id, name = 'trening_id')
]
