from django import forms
from .models import TraduccionIA

class TraduccionIAForm(forms.ModelForm):
    class Meta:
        model = TraduccionIA
        fields = ['texto_original', 'idioma_origen', 'idioma_destino']
        widgets = {
            'texto_original': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'idioma_origen': forms.TextInput(attrs={'class': 'form-control'}),
            'idioma_destino': forms.TextInput(attrs={'class': 'form-control'}),
        }
