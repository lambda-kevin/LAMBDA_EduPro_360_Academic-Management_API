from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser, Rol, Permiso, UsuarioRol


# ----------------------------
# Formularios personalizados
# ----------------------------

class FormularioCreacionUsuario(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("correo", "nombre", "apellido", "rol", "estado")

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return p2

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password1"])
        if commit:
            usuario.save()
        return usuario


class FormularioCambioUsuario(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Contraseña"),
        help_text=_("Las contraseñas no se muestran. Usa 'change password' para cambiarla.")
    )

    class Meta:
        model = CustomUser
        fields = (
            "correo", "nombre", "apellido", "password",
            "rol", "estado", "is_active", "is_staff", "is_superuser"
        )

    def clean_password(self):
        return self.initial["password"]


# ----------------------------
# Admin para CustomUser
# ----------------------------

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = FormularioCambioUsuario
    add_form = FormularioCreacionUsuario

    list_display = (
        "correo", "nombre", "apellido",
        "rol", "estado",
        "is_active", "is_staff", "is_superuser",
        "fecha_creacion"
    )

    list_filter = ("estado", "rol", "is_staff", "is_superuser")

    fieldsets = (
        (None, {"fields": ("correo", "password")}),
        ("Información Personal", {"fields": ("nombre", "apellido", "rol", "estado")}),
        ("Permisos", {"fields": (
            "is_active", "is_staff", "is_superuser",
            "groups", "user_permissions"
        )}),
        ("Metadatos", {"fields": ("fecha_creacion",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("correo", "nombre", "apellido", "rol",
                       "password1", "password2", "estado"),
        }),
    )

    search_fields = ("correo", "nombre", "apellido")
    ordering = ("correo",)
    filter_horizontal = ("groups", "user_permissions")


# ----------------------------
# Registrar Roles y Permisos
# ----------------------------

admin.site.register(Rol)
admin.site.register(Permiso)
admin.site.register(UsuarioRol)
