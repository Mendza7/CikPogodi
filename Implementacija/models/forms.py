#Autor: Mehmed Harcinovic 0261/19
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *


User = get_user_model()

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['username','email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


class KorisnikAdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','tipkorisnika']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class KorisnikAdminChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_active', 'tipkorisnika', 'is_superuser']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RecCreationForm(forms.ModelForm):
    class Meta:
        model = Rec
        fields= ['rec','tezina']

    def clean_tezina(self):
        rec = self.cleaned_data['rec']
        tezina = 0
        if len(rec) <8 :
            tezina = Rec.LAKA
            return tezina
        elif len(rec) < 13:
            tezina = Rec.SREDNJA
            return tezina
        else:
            tezina = Rec.TESKA
            return tezina

    def clean_rec(self):
        rec = self.cleaned_data.get('rec')

        qs = Rec.objects.filter(rec=rec)
        if qs.exists():
            raise forms.ValidationError("rec already exists")
        return rec

    def save(self,commit = True):
        rec = Rec.create(self.cleaned_data['rec'])
        rec.save()


class RecChangeForm(forms.ModelForm):

    class Meta:
        model=Rec
        fields = ['rec', 'tezina']

    def clean_rec(self):
        rec= self.cleaned_data['rec']
        if len(rec)==0:
            raise forms.ValidationError("prazna rec")

        qs = Rec.objects.filter(rec=rec)
        if qs.exists():
            raise forms.ValidationError("rec already exists")

        return rec

    def clean_tezina(self):
        rec = self.cleaned_data['rec']
        tezina = 0
        if len(rec) <8 :
            tezina = Rec.LAKA
            return tezina
        elif len(rec) < 13:
            tezina = Rec.SREDNJA
            return tezina
        else:
            tezina = Rec.TESKA
            return tezina