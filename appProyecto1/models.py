from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings 
class Institucion(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    nivel_tecnologico = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    region = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=20, blank=True)
    rut = models.CharField(max_length=30, unique=True)
    contacto = models.CharField(max_length=200, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='pacientes')
    identificador_nacional = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class SistemaOrigen(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100, blank=True)
    protocolo = models.CharField(max_length=100, blank=True)
    contacto = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre


class DocumentoClinico(models.Model):
    sistema = models.ForeignKey(SistemaOrigen, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.CharField(max_length=150)
    fecha_emision = models.DateField()
    autor = models.CharField(max_length=200, blank=True)
    formato = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.tipo_documento} - {self.fecha_emision}"


class DatosClinicos(models.Model):
    documento = models.ForeignKey(DocumentoClinico, on_delete=models.CASCADE, related_name='datos')
    campo_original = models.CharField(max_length=200)
    valor_original = models.TextField()
    valor_estandarizado = models.TextField(null=True, blank=True)
    fecha_registro = models.DateField()
    fuente = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.campo_original}: {self.valor_original[:40]}"


class EpisodioClinico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='episodios')
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(null=True, blank=True)
    tipo_acceso = models.CharField(max_length=100, blank=True)
    diagnostico_principal = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Episodio {self.id} - {self.paciente}"


class AccesoSeguridad(models.Model):
    usuario = models.CharField(max_length=200)
    rol = models.CharField(max_length=100, blank=True)
    fecha_acceso = models.DateTimeField(auto_now_add=True)
    tipo_acceso = models.CharField(max_length=100, blank=True)
    log_acciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.fecha_acceso}"


class MedicalTerm(models.Model):
    code = models.CharField(max_length=100)
    system = models.CharField(max_length=50)
    preferred_term = models.CharField(max_length=255)
    synonyms = models.TextField(blank=True)
    language = models.CharField(max_length=10, default='es')

    class Meta:
        unique_together = ('code', 'system')

    def __str__(self):
        return f"{self.preferred_term} ({self.system}:{self.code})"



class TraduccionIA(models.Model):
    usuario = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='traducciones',
    null=True,
    blank=True
)
    texto_original = models.TextField()
    texto_traducido = models.TextField()
    idioma_origen = models.CharField(max_length=50)
    idioma_destino = models.CharField(max_length=50)
    fecha_proceso = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.idioma_origen} → {self.idioma_destino}"

class FHIRObservation(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='observaciones_fhir')
    traduccion = models.ForeignKey(TraduccionIA, on_delete=models.CASCADE, null=True, blank=True)
    documento = models.ForeignKey(DocumentoClinico, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, default='final')
    categoria = models.CharField(max_length=50, default='translation')
    codigo = models.CharField(max_length=100, default='Texto médico traducido')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FHIR Observation - {self.id} ({self.paciente})"

    def to_fhir_json(self):
        return {
            "resourceType": "Observation",
            "id": str(self.id),
            "status": self.status,
            "category": [{"text": self.categoria}],
            "code": {"text": self.codigo},
            "subject": {
                "reference": f"Patient/{self.paciente.id}",
                "display": f"{self.paciente.nombre} {self.paciente.apellido}"
            },
            "effectiveDateTime": self.fecha_creacion.isoformat(),
            "valueString": self.traduccion.texto_traducido if self.traduccion else "Sin traducción",
            "note": [{
                "text": f"Documento clínico asociado: {self.documento}" if self.documento else "Sin documento asociado"
            }]
        }


class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id) +" " + self.name + "($" + str(self.salary) + ")"




class Usuario(AbstractUser):
    rol = models.CharField(
        max_length=30, 
        choices=[("doctor","Doctor"), ("administrador","Administrador")],
        default="doctor"
    )






User = get_user_model()

class Notificacion(models.Model):
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.email} - {self.mensaje}"

