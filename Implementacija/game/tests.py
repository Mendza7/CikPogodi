from django.test import TestCase, Client
from django.urls import reverse

from models.models import *

# Create your tests here.

class GameTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin = Korisnik.objects.create_superuser(username='admin', email = 'admin@admin.com', password='adminadmir')

        self.u1 = Korisnik.objects.create_user(username='test', email='test@test.com', password='testic1234',
                                               tipKorisnika='osnovni')
        self.u2 = Korisnik.objects.create_user(username='test1', email='test1@test.com', password='testic1234',
                                               tipKorisnika='osnovni')

        self.i1 = Igra.create_igra(Igra.PVP)

        self.r1 = Rec.create("rec1")
        self.r2 = Rec.create("rec2")

        self.p1 = Partija.objects.create(idigra=self.i1, idrec1=self.r1, idrec2=self.r2, idkor1=self.u1,
                                         idkor2=self.u2)

        self.l1 = Lobi.objects.create(ime='TestLobi', idpartija=self.p1, idkor1=self.u1, idkor2=self.u2)
        self.l1.save()

        self.l2 = Lobi.objects.create(ime="VipTestLobi", tip=Lobi.VIP, idpartija=self.p1, idkor1=self.u1,
                                      idkor2=self.u2)
        self.l2.save()


    def test_game_join_admin(self):
        self.client.login(username='admin', password='adminadmir')
        response = self.client.get(reverse('game_id', args=(1,)),follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_game_join_user(self):
        self.client.login(username='test', password='testic1234')
        response = self.client.get(reverse('game_id', args=(1,)), follow=True)
        self.assertEqual(response.status_code, 200)



