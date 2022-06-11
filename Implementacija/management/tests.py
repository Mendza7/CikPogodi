from django.test import TestCase,Client
from django.urls import reverse

from models.models import *
# Create your tests here.

class RegistrationTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def tearDown(self) -> None:
        pass

    def test_registration_no_data(self):
        response =self.client.post(reverse('registracija'),data={'email':'', 'korisnickoime':'', 'lozinka':''})
        self.assertContains(response,"Neispravno korisnicko ime ili vec postoji korisnik sa tim korisnickim imenom")

    def test_registration_no_email(self):
        response = self.client.post(reverse('registracija'),
                                    data={'email': '', 'korisnickoime': 'testic', 'lozinka': 'test123'})
        self.assertContains(response, "Neispravan email ili vec postoji korisnik")

    def test_registration_no_username(self):
        response = self.client.post(reverse('registracija'),
                                    data={'email': 'testic123@gmail.com', 'korisnickoime': '', 'lozinka': 'test123'})
        self.assertContains(response, "Neispravno korisnicko ime ili vec postoji korisnik sa tim korisnickim imenom")


    def test_registration_no_password(self):
        response = self.client.post(reverse('registracija'),
                                    data={'email': 'testic123@gmail.com', 'korisnickoime': 'test', 'lozinka': ''})
        self.assertContains(response, "Unesite lozinku")

    def test_registration_success(self):
        response = self.client.post(reverse('registracija'),
                                    data={'email': 'testic123@gmail.com', 'korisnickoime': 'test', 'lozinka': 'test123'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(Korisnik.objects.count(),1)
        self.assertEqual(Igrac.objects.count(),1)




class RankListTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirect(self):
        response = self.client.get(reverse('rang-lista'))
        self.assertRedirects(response,'/prijava?next=/rang-lista')

    def test_user_count(self):
        self.client.login(username ='test', password = 'password')
        self.igrac = Igrac.create(
            Korisnik.objects.create_user(username = 'test', email = 'test@test.com', password='testic1234', tipKorisnika='osnovni'))
        response = self.client.get(reverse('rang-lista'),follow=True)

        self.assertEqual(Igrac.objects.count(),1)
        self.assertEqual(response.status_code,200)


class izborLobijaTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.u1 = Korisnik.objects.create_user(username='test', email='test@test.com', password='testic1234',
                                               tipKorisnika='osnovni')
        self.u2 = Korisnik.objects.create_user(username='test1', email='test1@test.com', password='testic1234',
                                               tipKorisnika='osnovni')

        self.i1 = Igra.create_igra(Igra.PVP)

        self.r1 = Rec.create("rec1")
        self.r2 = Rec.create("rec2")

        self.p1 = Partija.objects.create(idigra=self.i1, idrec1=self.r1, idrec2=self.r2, idkor1=self.u1, idkor2=self.u2)

        self.l1 = Lobi.objects.create(ime='TestLobi', idpartija=self.p1, idkor1=self.u1, idkor2=self.u2)
        self.l1.save()

        self.l2 = Lobi.objects.create(ime="VipTestLobi", tip=Lobi.VIP, idpartija=self.p1, idkor1=self.u1,
                                      idkor2=self.u2)
        self.l2.save()


    def test_izbor_lobija(self):
        self.client.login(username = "test", password = "testic1234")
        response = self.client.get(reverse('izbor-lobija'),follow=True)
        self.assertEqual(response.status_code,200)
        self.assertEqual(Lobi.objects.filter(tip = Lobi.VIP).count(),1)
        self.assertEqual(Lobi.objects.filter(tip = Lobi.OSNOVNI).count(),1)




