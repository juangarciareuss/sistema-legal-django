# config/urls.py

from django.contrib import admin
from django.urls import path, include  # <-- Asegúrate de añadir 'include'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Esta línea le dice al proyecto que cualquier URL que empiece con 'causas/'
    # debe ser manejada por el archivo urls.py de nuestra app 'causas'.
    path('causas/', include('causas.urls')),  # <-- AÑADE ESTA LÍNEA
]
