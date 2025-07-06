# causas/urls.py

from django.urls import path
# Ahora importamos la nueva vista también
from .views import (
    lista_causas, 
    detalle_causa, 
    CausaCreateView, 
    CausaUpdateView, 
    CausaDeleteView
)

urlpatterns = [
    # Cuando la URL esté vacía (la raíz de la app 'causas'),
    # llamará a la vista 'lista_causas'.
    # Le damos un nombre 'lista_causas' para poder referenciarla fácilmente más tarde.
    path('', lista_causas, name='lista_causas'),

    # Esta URL captura un número entero (int) de la dirección
    # y lo pasa a la vista como una variable llamada 'pk'.
    path('<int:pk>/', detalle_causa, name='detalle_causa'),

    path('nueva/', CausaCreateView.as_view(), name='crear_causa'),
    path('<int:pk>/editar/', CausaUpdateView.as_view(), name='editar_causa'),
    path('<int:pk>/eliminar/', CausaDeleteView.as_view(), name='eliminar_causa'),
]