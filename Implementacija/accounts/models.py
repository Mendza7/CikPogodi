from random import randint, random

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
# Create your models here.
from CikPogodi import settings


class KorisnikManager(BaseUserManager):

    def create_user(self, username: object, email: object, password: object = None, **extra_fields: object) -> object:
        if not username or not email:
            raise ValueError("korisnickoime prazno.")

        tip = 'osnovni'
        if extra_fields['tipKorisnika'] in ['osnovni', 'vip']:
            tip = extra_fields['tipKorisnika']

        korisnik = Korisnik(
            username=username,
            email=email,
            tipkorisnika=tip
        )
        korisnik.set_password(password)
        korisnik.save()

        return korisnik

    def create_staffuser(self, username, email, password=None, **extra_fields):
        if not username or not email:
            raise ValueError("korisnickoime prazno.")

        korisnik = Korisnik(
            username=username,
            email=email,
            tipkorisnika='admin'
        )
        korisnik.is_staff=1
        korisnik.set_password(password)
        korisnik.save()

        return korisnik

    def create_superuser(self, username, email, password=None, **extra_fields):
        if not username or not email:
            raise ValueError("korisnickoime prazno.")

        korisnik = self.model(
            username=username,
            email=email,
            tipkorisnika='admin'
        )
        korisnik.is_superuser=1
        korisnik.is_staff=1
        korisnik.set_password(password)
        korisnik.save()

        return korisnik

    def postoji_korisnik(self, korisnickoime, email):
        return self.filter(username=korisnickoime, email=email).exists()

    def postoji_korisnik_email(self, email):
        return self.filter(email=email).exists()


class Korisnik(AbstractUser):
    OSNOVNI = 'osnovni'
    VIP = 'vip'
    ADMIN = 'admin'

    objects = KorisnikManager()

    TIP = [
        (OSNOVNI, _('Osnovni korisnik')),
        (VIP, _('VIP korisnik')),
        (ADMIN, _('Administrator')),
    ]

    idkor = models.AutoField(db_column='idKor', primary_key=True)  # Field name made lowercase.
    tipkorisnika = models.CharField(db_column='tipKorisnika', max_length=45,
                                    choices=TIP,
                                    default=OSNOVNI,
                                    null=False)  # Field name made lowercase.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']

    class Meta:
        db_table = 'Korisnik'

    # trebalo bi da se ovo vec radi automatski
    # @staticmethod
    # def generisi_lozinku():
    #     characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    #     random.shuffle(characters)
    #
    #     nova_lozinka = []
    #     for i in range(8):
    #         nova_lozinka.append(random.choice(characters))
    #
    #     random.shuffle(nova_lozinka)
    #
    #     return "".join(nova_lozinka)

    # ima authenticate()
    # @staticmethod
    # def proveri_kredencijale(korisnicko_ime, lozinka):
    #     hash_lozinka = hashlib.md5(lozinka.encode('utf-8'))
    #     return Korisnik.objects.filter(korisnickoime=korisnicko_ime, lozinka=hash_lozinka).exists()

    # @staticmethod
    # def promeni_lozinku(email, nova_lozinka):
    #     hash_lozinka = hashlib.md5(nova_lozinka.encode('utf-8'))
    #     k = Korisnik.objects.filter(email=email).get()
    #     k.lozinka = hash_lozinka.hexdigest()
    #     k.save()
    #     return nova_lozinka


class Igrac(models.Model):
    idkor = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE, db_column='idKor',
                                 primary_key=True)  # Field name made lowercase.
    brojpartija = models.IntegerField(db_column='brojPartija')  # Field name made lowercase.
    brojpobeda = models.IntegerField(db_column='brojPobeda')  # Field name made lowercase.
    blokiran = models.IntegerField()

    class Meta:
        db_table = 'Igrac'

    @staticmethod
    def create(idkor):
        igrac = Igrac(
            idkor=idkor,
            brojpartija=0,
            brojpobeda=0,
            blokiran=0
        )
        igrac.save()
        return igrac


class Rec(models.Model):
    LAKA = 0
    SREDNJA = 1
    TESKA = 2

    TEZINA = [
        (LAKA, _('Laka rec')),
        (SREDNJA, _('Srednja rec')),
        (TESKA, _('Teska rec')),
    ]

    idrec = models.AutoField(db_column='idRec', primary_key=True)
    rec = models.CharField(max_length=45,null=False, unique=True)
    tezina = models.IntegerField(choices=TEZINA, null = True)

    class Meta:
        db_table='rec'


    def __str__(self):
        return self.rec

    @staticmethod
    def create(recString):
        if (len(recString) <= 6):
            tezina = 0
        elif (len(recString) > 6 and len(recString) <= 9):
            tezina = 1
        else:
            tezina = 2

        rec = Rec(
            rec=recString,
            tezina=tezina
        )
        rec.save()
        return rec



class Igra(models.Model):
    TRENING = 'trening'
    PVP = 'duel'

    TIP = [
        (TRENING, _('Trening')),
        (PVP, _('Duel')),
    ]

    ISHOD = [
        (-2,_('U toku')),
        (-1,_('Igrac 1 pobeda')),
        (0,_('Nereseno')),
        (1,_('Igrac 2 pobeda')),
    ]
    idigra = models.AutoField(db_column='idIgra', primary_key=True)
    tipigre = models.CharField(max_length=45, choices=TIP)
    ishod = models.IntegerField(choices=ISHOD, default=-2)

    class Meta:
        db_table='Igra'

    @staticmethod
    def create_igra(tipIgre):
        igra = Igra(tipigre = tipIgre,ishod = -2)
        igra.save()
        return igra




class Trening(models.Model):
    idigra = models.OneToOneField(Igra, models.CASCADE,to_field='idigra')
    idrec=models.ForeignKey(Rec, models.DO_NOTHING,to_field='idrec')
    idkor = models.ForeignKey(settings.AUTH_USER_MODEL,models.DO_NOTHING,to_field='idkor')

    class Meta:
        db_table='Trening'

    @staticmethod
    def create_trening(idkor,rec):
        tren = Trening(idigra=Igra.create_igra(Igra.TRENING),idrec = rec, idkor = idkor)
        tren.save()
        return tren



class Lobi(models.Model):
    OSNOVNI = 'osnovni'
    VIP = 'vip'

    TIP = [
        (OSNOVNI, _('Osnovni korisnik')),
        (VIP, _('VIP korisnik')),
    ]

    U_TOKU = 'u toku'
    OTVOREN = 'otvoren'

    STATUS = [
        (OTVOREN,_('Otvoren lobi')),
        (U_TOKU,_('Igra u toku'))
    ]

    idigra = models.OneToOneField(Igra, models.CASCADE,to_field='idigra',primary_key=True)
    tip = models.CharField(choices=TIP,default=OSNOVNI, null = False, max_length=30)
    status = models.CharField(choices=STATUS,default=OTVOREN, max_length=30)

    idkor1 = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name="%(class)s_idkor1")
    idkor2 = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name="%(class)s_idkor2")



    class Meta:
        db_table='lobi'


class Potez(models.Model):
    idpotez = models.AutoField(db_column = "idPotez", primary_key = True)
    idigra = models.ForeignKey(Igra, models.CASCADE,to_field='idigra')
    idkor = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name="%(class)s_idkor+")
    idrec = models.ForeignKey(Rec,models.DO_NOTHING,related_name="%(class)s_idrec+", default=-1)
    slovo = models.CharField(max_length=1,null=False, default="#")
    ishod = models.BooleanField(null=False)

    class Meta:
        db_table='potez'




class Partija(models.Model):
    idigra = models.OneToOneField(Igra, models.CASCADE,to_field='idigra',primary_key=True)
    first_turn = models.IntegerField(default = randint(0,1))

    idrec1 = models.ForeignKey(Rec,models.DO_NOTHING, related_name="idrec1")
    idrec2 = models.ForeignKey(Rec,models.DO_NOTHING, related_name="idrec2")

    idkor1 = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name="idkor1")
    idkor2 = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, related_name="idkor2")

    brojzivota1 = models.IntegerField()
    brojzivota2 = models.IntegerField()

    idlobi = models.ForeignKey(Lobi,models.DO_NOTHING)

    class Meta:
        db_table='Partija'



# def create_administrator(korisnickoime, lozinka, email, ime, prezime):
#     korisnik = Korisnik.create(korisnickoime, lozinka, email, Korisnik.Tip.admin)
#     admin = Administrator.create(korisnik, ime, prezime)
#     return True
#
#
# def create_igrac(korisnickoime, lozinka, email):
#     if not Korisnik.postoji_korisnik(korisnickoime, email):
#         korisnik = Korisnik.create(korisnickoime, lozinka, email, Korisnik.Tip.igrac)
#         igrac = Igrac.create(korisnik)
#         return True
#     else:
#         return False
