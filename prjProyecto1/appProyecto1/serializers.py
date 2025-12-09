from rest_framework import serializers
from .models import DatosClinicos, TraduccionIA

class TranslateRequestSerializer(serializers.Serializer):
    source_language = serializers.CharField()
    target_language = serializers.CharField()
    text = serializers.CharField()
    paciente_rut = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    documento_id = serializers.IntegerField(required=False, allow_null=True)

class TraduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraduccionIA
        fields = '__all__'

class DatosClinicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosClinicos
        fields = '__all__'

