from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from .models import (
    Usuario,
    TraduccionIA,
    FHIRObservation,
    Paciente,
    Notificacion
)

# ---------------------------------------------
# 🔹 1. Crear FHIR Observation al crear una traducción
# ---------------------------------------------
@receiver(post_save, sender=TraduccionIA)
def crear_fhir_observation(sender, instance, created, **kwargs):
    if created:
        paciente = Paciente.objects.first()
        if not paciente:
            print("⚠ No hay pacientes registrados, no se puede crear FHIRObservation.")
            return

        obs = FHIRObservation.objects.create(
            paciente=paciente,
            traduccion=instance,
            status='final',
            categoria='translation',
            codigo='Traducción automática'
        )

        print(f"✔ FHIRObservation creada (ID {obs.id}) para la traducción {instance.id}")


# ---------------------------------------------
# 🔹 2. Asignar permisos al crear un usuario
# ---------------------------------------------
@receiver(post_save, sender=Usuario)
def asignar_permisos_usuario(sender, instance, created, **kwargs):
    if created:
        if instance.rol == "doctor":
            permisos = Permission.objects.filter(
                codename__in=[
                    "add_traduccionia",
                    "change_traduccionia",
                    "delete_traduccionia",
                ]
            )
            instance.user_permissions.set(permisos)

        if instance.rol == "admin":
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()


User = get_user_model()

# ---------------------------------------------
# 🔹 3. Notificación cuando se crea un usuario nuevo
# ---------------------------------------------
@receiver(post_save, sender=User)
def notificar_usuario_creado(sender, instance, created, **kwargs):
    if created:
        Notificacion.objects.create(
            mensaje=f"Nuevo usuario registrado: {instance.username}",
            usuario=instance
        )


# ---------------------------------------------
# 🔹 4. Notificación cuando se crea una traducción
# ---------------------------------------------
@receiver(post_save, sender=TraduccionIA)
def notificar_traduccion_creada(sender, instance, created, **kwargs):
    if created:
        usuario = instance.usuario

        mensaje = (
            f"El usuario {usuario.username} realizó una nueva traducción."
            if usuario else
            "Se creó una nueva traducción (usuario no especificado)."
        )

        Notificacion.objects.create(
            mensaje=mensaje,
            usuario=usuario if usuario else None
        )
