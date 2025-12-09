from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import (
    Institucion, Paciente, SistemaOrigen, DocumentoClinico, DatosClinicos,
    TraduccionIA, EpisodioClinico, AccesoSeguridad, MedicalTerm, Usuario
)

# ============================
#  FORMULARIOS PERSONALIZADOS
# ============================

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'email', 'rol')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'rol', 'is_staff', 'is_active')


# ============================
#   ADMIN PERSONALIZADO
# ============================

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario

    list_display = ('username', 'email', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('email',)}),
        ('Rol del usuario', {'fields': ('rol',)}),
        ('Permisos', {
            'fields': (
                'is_staff', 'is_active', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'rol',
                'password1', 'password2',
                'is_staff', 'is_active'
            )
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)


# Otros modelos del admin
admin.site.register(Institucion)
admin.site.register(Paciente)
admin.site.register(SistemaOrigen)
admin.site.register(DocumentoClinico)
admin.site.register(DatosClinicos)
admin.site.register(TraduccionIA)
admin.site.register(EpisodioClinico)
admin.site.register(AccesoSeguridad)
admin.site.register(MedicalTerm)
