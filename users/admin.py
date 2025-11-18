from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

# Si tienes un modelo Role en tu app, se intentará registrarlo más abajo
try:
    from .models import Role
except Exception:
    Role = None


# ----------------------------
# Formularios personalizados
# ----------------------------

class FormularioCreacionUsuario(forms.ModelForm):
    """
    Formulario para crear usuarios en el admin.
    Muestra password en dos campos y guarda el hash con set_password.
    """
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
    """
    Formulario para actualizar usuarios en el admin.
    Muestra la contraseña como campo de sólo lectura (hash).
    """
    password = ReadOnlyPasswordHashField(label=_("Contraseña"),
        help_text=_("Las contraseñas no se muestran. Usa 'change password' para cambiarla."))

    class Meta:
        model = CustomUser
        fields = ("correo", "nombre", "apellido", "password", "rol", "estado", "is_active", "is_staff", "is_superuser")

    def clean_password(self):
        # Devuelve el valor original, no el proporcionado por el form
        return self.initial["password"]


# ----------------------------
# Admin personalizado
# ----------------------------

class CustomUserAdmin(BaseUserAdmin):
    form = FormularioCambioUsuario
    add_form = FormularioCreacionUsuario

    # Campos mostrados en la lista
    list_display = ("correo", "nombre", "apellido", "rol", "estado", "is_staff", "is_superuser", "fecha_creacion")
    list_filter = ("is_staff", "is_superuser", "estado", "rol")

    # Organización de campos en la vista detalle
    fieldsets = (
        (None, {"fields": ("correo", "password")}),
        ("Información personal", {"fields": ("nombre", "apellido", "rol")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Metadatos", {"fields": ("estado", "fecha_creacion")}),
    )

    # Campos para crear un usuario desde el admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("correo", "nombre", "apellido", "rol", "password1", "password2", "estado"),
        }),
    )

    search_fields = ("correo", "nombre", "apellido")
    ordering = ("correo",)
    filter_horizontal = ("groups", "user_permissions",)


# Registrar el CustomUser en el admin
admin.site.register(CustomUser, CustomUserAdmin)


# Registrar Role si existe
if Role is not None:
    try:
        admin.site.register(Role)
    except admin.sites.AlreadyRegistered:
        pass
