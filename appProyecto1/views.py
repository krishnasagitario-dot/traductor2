from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json

# MODELOS
from .models import (
    Employee,
    TraduccionIA,
    FHIRObservation,
    Paciente,
    Usuario,
    Notificacion
)

# SERVICIOS
from .services.openai_service import translate_medical_text

# ========== FUNCIONES DE ROL ==========

def es_doctor(user):
    return user.groups.filter(name='Doctor').exists()

def es_admin(user):
    return user.groups.filter(name='Administrador').exists()


# ========== HOME SEGÚN ROL ==========

@login_required
def home(request):
    user = request.user

    if es_admin(user):
        return redirect("manage_translations")

    if es_doctor(user):
        return redirect("translator_page")

    return redirect("translator_page")


# ========== API DE TRADUCCIÓN ==========

@csrf_exempt
@login_required
def api_translate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("text", "")
        source_specialty = data.get("source_specialty", "")
        target_specialty = data.get("target_specialty", "")

        # Traducción simulada
        translated = f"[{target_specialty}] Traducción de: {text}"

        # Guardar traducción
        traduccion = TraduccionIA.objects.create(
            texto_original=text,
            texto_traducido=translated,
            idioma_origen=source_specialty,
            idioma_destino=target_specialty,
            usuario=request.user
        )

        # Crear notificación correcta
        Notificacion.objects.create(
            mensaje=f"El usuario {request.user.username} creó una nueva traducción.",
            usuario=request.user
        )

        return JsonResponse({
            "translated_text": translated,
            "id": traduccion.id
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)

# ========== EDITAR ==========

def edit_traduccion(request, pk):
    traduccion = get_object_or_404(TraduccionIA, pk=pk)

    if request.method == "POST":
        texto_original = request.POST.get("texto_original", traduccion.texto_original)
        idioma_origen = request.POST.get("idioma_origen", traduccion.idioma_origen)
        idioma_destino = request.POST.get("idioma_destino", traduccion.idioma_destino)

        traduccion.texto_traducido = translate_medical_text(texto_original)
        traduccion.texto_original = texto_original
        traduccion.idioma_origen = idioma_origen
        traduccion.idioma_destino = idioma_destino
        traduccion.save()

        return redirect('translator_page')

    return render(request, 'traductor/edit_traducciones.html', {"traduccion": traduccion})


# ========== ELIMINAR ==========

def delete_traduccion(request, pk):
    traduccion = get_object_or_404(TraduccionIA, pk=pk)
    traduccion.delete()
    return redirect('translator_page')


# ========== EXPORTAR FHIR ==========

def exportar_fhir_observation(request, pk):
    obs = get_object_or_404(FHIRObservation, pk=pk)
    return JsonResponse(
        obs.to_fhir_json(),
        safe=False,
        json_dumps_params={'ensure_ascii': False, 'indent': 2}
    )


# ========== API REST ==========

class TranslateAPIView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        source_specialty = request.data.get('source_specialty', 'Medicina General')
        target_specialty = request.data.get('target_specialty', 'Medicina General')

        if not text.strip():
            return Response({"error": "Texto vacío"}, status=status.HTTP_400_BAD_REQUEST)

        translated_text = translate_medical_text(
            f"Traduce este texto desde {source_specialty} hacia {target_specialty}:\n{text}"
        )

        trad = TraduccionIA.objects.create(
            texto_original=text,
            texto_traducido=translated_text,
            idioma_origen=source_specialty,
            idioma_destino=target_specialty,
            usuario=request.user

        )

        return Response({
            "translated_text": translated_text,
            "id": trad.id
        }, status=status.HTTP_201_CREATED)


# ========== LISTADOS JSON ==========

def list_observations(request):
    observations = list(FHIRObservation.objects.values())
    return JsonResponse(observations, safe=False)

def listar_pacientes(request):
    pacientes = list(Paciente.objects.values())
    return JsonResponse(pacientes, safe=False)


# ========== EMPLEADOS ==========

def EmployeeViews(request):
    emp = {
        'id': 123,
        'name': 'krishna',
        'email': 'krishna@example.com',
        'salary': 500
    }
    return JsonResponse(emp)

def EmployeeView(request):
    empleados = Employee.objects.all()
    data = {'employees': list(empleados.values('name', 'salary'))}
    return JsonResponse(data)


# ========== REGISTRO DE USUARIOS ==========
UsuarioModel = get_user_model()

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        rol = request.POST.get("rol")

        # Validar contraseñas
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register_user")

        # Validar nombre de usuario existente
        if UsuarioModel.objects.filter(username=username).exists():
            messages.error(request, "Este usuario ya existe.")
            return redirect("register_user")

        # Crear usuario
        user = UsuarioModel.objects.create_user(
            username=username,
            email=email,
            password=password1,
            rol=rol
        )

        # Crear notificación según tu modelo actual
        Notificacion.objects.create(
            mensaje=f"El usuario {user.username} se ha registrado.",
            usuario=user
        )

        messages.success(request, "Usuario creado correctamente.")
        return redirect("manage_translations")
 
    return render(request, "traductor/register.html")

# ========== LOGIN ==========

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "traductor/login.html")


# ========== LOGOUT ==========

def logout_user(request):
    logout(request)
    return redirect("login_user")


# ========== TRADUCIR TEXTO (Doctor) ==========

def traducir_texto(texto, origen, destino):
    return f"[Traducción simulada de {origen} a {destino}]: {texto}"


@login_required
def translate_text(request):
    if request.method == "POST":
        texto = request.POST.get("texto")
        idioma_origen = request.POST.get("idioma_origen")
        idioma_destino = request.POST.get("idioma_destino")

        texto_traducido = traducir_texto(texto, idioma_origen, idioma_destino)

        traduccion = TraduccionIA.objects.create(
            texto_original=texto,
            texto_traducido=texto_traducido,
            idioma_origen=idioma_origen,
            idioma_destino=idioma_destino,
            usuario=request.user
        )

        # Notificación 
        Notificacion.objects.create(
            mensaje=f"El usuario {request.user.username} realizó una traducción.",
            usuario=request.user
        )

        return render(request, "traductor/traducir.html", {
            "texto_traducido": texto_traducido
        })

    return render(request, "traductor/traducir.html")


# ========== ADMIN: VER TODAS LAS TRADUCCIONES ==========

@login_required
@user_passes_test(es_admin)
def manage_translations(request):
    traducciones = TraduccionIA.objects.all().order_by('-fecha_proceso')
    return render(request, "traductor/admin_traducciones.html", {
        "traducciones": traducciones
    })


# ========== DOCTOR/ADMIN: PANTALLA DEL TRADUCTOR ==========

@login_required
def translator_page(request):
    traducciones = TraduccionIA.objects.all().order_by('-fecha_proceso')
    return render(request, "traductor/translator.html", {
        "user": request.user,
        "traducciones": traducciones
    })


# ========== ADMIN NOTIFICACIONES ==========
@login_required
@user_passes_test(es_admin)
def admin_notificaciones(request):
    notificaciones = Notificacion.objects.order_by('-fecha')
    return render(request, "notificaciones/panel_admin.html", {"notificaciones": notificaciones})



# ========== MARCAR COMO LEÍDA ==========

@login_required
def mark_notificacion_read(request, pk):
    notif = get_object_or_404(Notificacion, id=pk)
    notif.leida = True
    notif.save()
    return redirect("admin_notificaciones")


# ========== API JSON DE NOTIFICACIONES ==========

def api_notificaciones(request):
    notificaciones = list(Notificacion.objects.values())
    return JsonResponse(notificaciones, safe=False)





def notificaciones_home(request):
    return render(request, 'notificaciones/panel_admin.html')




