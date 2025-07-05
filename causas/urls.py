# causas/urls.py

from django.urls import path
# Ahora importamos la nueva vista también
from .views import lista_causas, detalle_causa, CausaCreateView

urlpatterns = [
    # Cuando la URL esté vacía (la raíz de la app 'causas'),
    # llamará a la vista 'lista_causas'.
    # Le damos un nombre 'lista_causas' para poder referenciarla fácilmente más tarde.
    path('', lista_causas, name='lista_causas'),

    # Esta URL captura un número entero (int) de la dirección
    # y lo pasa a la vista como una variable llamada 'pk'.
    path('<int:pk>/', detalle_causa, name='detalle_causa'),

    path('nueva/', CausaCreateView.as_view(), name='crear_causa'),
]