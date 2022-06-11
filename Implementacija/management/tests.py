# Autori: Merisa Harcinovic 0258/19,  Magdalena Cvorovic 0670/19, Mehmed Harcinovic 0261/19
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




class resetLozinkaTestPraznoPolje(TestCase):
    def setUp(self)->None:
        self.client = Client()

    def tearDown(self) ->None:
        pass
    def test_reset(self):
        response=self.client.post(reverse('reset-lozinke'), data = {'email': ''})
        self.assertContains(response, "Unesite email")

class resetLozinkaTestUspesno(TestCase):
    def setUp(self)->None:
        self.client = Client()
        self.user = Korisnik.objects.create_user('username1', 'email@gmail.com', 'password', tipKorisnika= 'osnovni')

    def test_reset_uspeh(self):
        response=self.client.post(reverse('reset-lozinke'), data = {'email': 'email@gmail.com'})
        self.assertContains(response, "Uskoro cete dobiti email sa novom lozinkom.")

class resetLozinkaTestNeispravanEmail(TestCase):
    def setUp(self)->None:
        self.client = Client()
        self.user = Korisnik.objects.create_user('username2', 'email@gmail.com', 'password', tipKorisnika= 'osnovni')

    def test_reset_neuspeh(self):
        response=self.client.post(reverse('reset-lozinke'), data = {'email': 'novi@gmail.com'})
        self.assertContains(response, "Korisnik sa unetim email-om ne postoji")

class odjavaUspesno(TestCase):
    def setUp(self)->None:
        self.client = Client()
        self.user = Korisnik.objects.create_user('username3', 'emailTest@mail.com', 'passwordTest',
                                                 tipKorisnika='osnovni')

    def test_odjava(self):
        self.client.login(username='username3', password='passwordTest')
        response = self.client.post(reverse('odjava'))
        self.assertContains(response, "Odjavljeni ste.")





class loginUspesno(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = Korisnik.objects.create_user('username5', 'emailTest@mail.com', 'passwordTest',
                                                 tipKorisnika='osnovni')

    def test_login(self):
        login = self.client.login(username='username5', password='passwordTest')

        self.assertTrue(login)

class loginNeuspesno(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = Korisnik.objects.create_user('username50', 'emailTest@mail.com', 'passwordTest',
                                                 tipKorisnika='osnovni')

    def test_login(self):
        login = self.client.login(username='username55', password='passwordTest')

        self.assertFalse(login)


class IndexTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
    def test_view_index_url(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(first=response.status_code, second=200)

class ManualTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
    def test_view_manual_url(self):
        response = self.client.get(reverse('uputstvo'))
        self.assertEqual(first=response.status_code, second=200)


class PrijavaTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user= Korisnik.objects.create_user('usernameTest', 'emailTest@mail.com', 'passwordTest', tipKorisnika='osnovni')

    def test_view_prijava_url(self):
        response = self.client.get(reverse('prijava'))
        self.assertEqual(first=response.status_code, second=200)


class KreirajLobiTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user= Korisnik.objects.create_user('usernameTest', 'emailTest@mail.com', 'passwordTest', tipKorisnika='osnovni')
        self.rec = Rec.create("recTest")
        self.adminTest2 = Korisnik.objects.create_superuser(username='adminTest2', email='atest@test.com',
                                                           password='admintest1234')
    def test_kreiraj_lobi_admin(self):
        self.client.login(username="adminTest2", password='admintest1234')
        response=self.client.get(reverse('kreiraj-lobi'))
        self.assertRedirects(response, reverse('index'))

    def test_kreiraj_lobi_no_data(self):
        self.client.login(username='usernameTest', password='passwordTest')
        response = self.client.post(reverse('kreiraj-lobi'), data={'imeLobija': '', 'selectedRec': ''})
        self.assertContains(response, "Morate uneti sve podatke.")

    def test_kreiraj_lobi_no_rec(self):
        self.client.login(username='usernameTest', password='passwordTest')
        response = self.client.post(reverse('kreiraj-lobi'), data={'imeLobija': 'LobiTest1', 'selectedRec': 'Odaberi rec'})
        self.assertContains(response, "Morate uneti sve podatke.")

    def test_kreiraj_lobi_no_lobi(self):
        self.client.login(username='usernameTest', password='passwordTest')
        response = self.client.post(reverse('kreiraj-lobi'), data={'imeLobija': '', 'selectedRec': 'recTest'})
        self.assertContains(response, "Morate uneti sve podatke.")

    def test_kreiraj_lobi(self):
        self.client.login(username='usernameTest', password='passwordTest')
        response = self.client.post(reverse('kreiraj-lobi'), data={'imeLobija': 'lobiTest', 'selectedRec': 'recTest'})
        self.assertEqual(Lobi.objects.count(),1)

class GostTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_gost_no_data(self):
        response= self.client.post(reverse('gost'), data={'gostime':''})
        self.assertContains(response, "Unesite ime")

    def test_gost(self):
        response= self.client.post(reverse('gost'), data={'gostime':'gostTest'})
        self.assertRedirects(response, '/izbor-rezima')

class SelectGameTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_selectgame_url(self):
        response = self.client.get(reverse('izbor-rezima'), follow=True)
        self.assertEqual(first=response.status_code, second=200)

class PridruziSeLobijuTest(TestCase):
    def setUp(self) -> None:
        self.adminTest = Korisnik.objects.create_superuser(username='adminTest1', email='atest@test.com', password='admintest1234')

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

    def test_adminTest(self):
        self.client.login(username="adminTest1", password="admintest1234")
        response= self.client.get(reverse('pridruzi-se', args={'id_lobi':2}), data={})
        self.assertRedirects(response, reverse('index'))
