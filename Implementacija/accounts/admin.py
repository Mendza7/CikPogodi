from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import *
from .forms import *


class KorisnikAdmin(UserAdmin):
    form = KorisnikAdminChangeForm
    add_form = KorisnikAdminCreationForm

    list_display = ['username','email','password']
    list_filter = ['tipkorisnika']
    fieldsets = (
        (None, {"fields": ("username", "password","tipkorisnika")}),
        (_("Personal info"), {"fields": ["email"]}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password", "password_2", "email", "tipkorisnika"),
            },
        ),
    )
    search_fields = ['username']
    ordering = ['username']
    filter_horizontal=()

class RecAdmin(ModelAdmin):
    add_form = RecCreationForm
    form = RecChangeForm
    list_filter = ['tezina']
    list_display = ['rec','tezina']
    search_fields = ['rec__contains']

    fields = ('rec',)


admin.site.register(Korisnik,KorisnikAdmin)
admin.site.register(Igrac)
admin.site.register(Rec,RecAdmin)
admin.site.register(Lobi)
