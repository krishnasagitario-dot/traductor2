import openai
from django.conf import settings
import os
import time
import random

def translate_medical_text(prompt):
    """
    Función simulada de traducción médica.
    Devuelve texto adaptado según palabras clave en el prompt.
    """

    # Simulación básica según especialidad
    if "Cardiología" in prompt:
        posibles = [
            "Paciente con dolor torácico y dificultad para respirar.",
            "Síntomas compatibles con infarto agudo al miocardio.",
            "Paciente presenta arritmia y requiere monitoreo cardíaco."
        ]
        return random.choice(posibles)

    elif "Neurología" in prompt:
        posibles = [
            "Paciente con cefalea intensa y mareos frecuentes.",
            "Presenta alteraciones en el sistema nervioso central.",
            "Se observan signos de neuropatía periférica."
        ]
        return random.choice(posibles)

    elif "Pediatría" in prompt:
        posibles = [
            "Paciente pediátrico con fiebre y tos persistente.",
            "Se observa erupción cutánea y malestar general.",
            "Niño presenta vómitos y diarrea desde hace 2 días."
        ]
        return random.choice(posibles)

    elif "Oncología" in prompt:
        posibles = [
            "Paciente con tumor sólido y requiere evaluación oncológica.",
            "Se sugiere iniciar protocolo de quimioterapia.",
            "Requiere seguimiento por posible metástasis."
        ]
        return random.choice(posibles)

    else:
        # Simulación genérica
        return "Texto traducido simulado: " + prompt[:50] + "..."

    ...
