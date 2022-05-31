from django.urls import path
from . import views

urlpatterns = [
    path('', views.Trening),
    path('<str:trening_id>/',views.trening_id, name = 'trening_id')
]
