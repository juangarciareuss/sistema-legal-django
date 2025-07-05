# causas/admin.py

from django.contrib import admin
from .models import Tribunal, Deudor, Causa

# Le decimos a Django que registre nuestros modelos en el sitio de administración.
# Cada línea crea una sección para gestionar el modelo correspondiente.
admin.site.register(Tribunal)
admin.site.register(Deudor)
admin.site.register(Causa)
