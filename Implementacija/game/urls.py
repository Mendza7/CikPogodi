#Autor: Mehmed Harcinovic 0261/19
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Game),
    path('<str:game_id>/',views.game_id, name = 'game_id'),
    path("get/ajax/<str:game_d>/",views.getWords, name = 'getWords'),
]