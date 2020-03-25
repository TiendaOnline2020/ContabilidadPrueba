from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User
# Register your models here.

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'password1', 'password2', 'empresa', 'email', 'periodo')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('empresa', 'periodo', 'email')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'is_staff']
    add_fieldsets = (
        ('Campos Usuario:', {
            'fields': ('username', ('password1', 'password2'), 'is_staff',)
        }),
        ('Datos Empresa:', {
            'fields': ('empresa', 'periodo')
        }),
    )
    fieldsets = (
        ('Campos Usuario:', {
            'fields': ('username', 'is_staff',)
        }),
        ('Datos Personales:', {
            'fields': (('empresa', 'periodo'),)
        }),
    )


admin.site.register(User, CustomUserAdmin)