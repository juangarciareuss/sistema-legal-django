# causas/forms.py
from django import forms
from .models import ArchivoAdjunto, Comentario, EtapaCausa 

class ArchivoAdjuntoForm(forms.ModelForm):
    class Meta:
        model = ArchivoAdjunto
        fields = ['archivo', 'etapa_causa', 'descripcion']
        widgets = {
            'etapa_causa': forms.HiddenInput(),
        }

# --- NUEVO FORMULARIO PARA COMENTARIOS ---
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto'] # Solo necesitamos mostrar el campo de texto
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu comentario aquí...'}),
        }
        labels = {
            'texto': '', # Opcional: quita la etiqueta "Texto:"
        }

class EtapaCausaForm(forms.ModelForm):
    class Meta:
        model = EtapaCausa
        fields = ['etapa', 'fecha', 'descripcion', 'costas']
        widgets = {
            'etapa': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Añade una descripción...'}),
            'costas': forms.NumberInput(attrs={'class': 'form-control'}),
        }