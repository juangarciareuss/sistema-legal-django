# causas/admin.py

from django.contrib import admin
from .models import (Tribunal, Deudor, Causa, 
                     Cartera, ArchivoAdjunto, Comentario,
                     AntecedentesLeasing, AntecedentesCBR, 
                     TipoEtapa, Etapa, EtapaCausa)


# Le decimos a Django que registre nuestros modelos en el sitio de administración.
# Cada línea crea una sección para gestionar el modelo correspondiente.
admin.site.register(Tribunal)
admin.site.register(Deudor)
admin.site.register(Causa)
admin.site.register(Cartera)
admin.site.register(ArchivoAdjunto)
admin.site.register(Comentario)
admin.site.register(AntecedentesLeasing)
admin.site.register(AntecedentesCBR)
admin.site.register(TipoEtapa)
admin.site.register(Etapa)
admin.site.register(EtapaCausa)