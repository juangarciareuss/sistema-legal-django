# causas/views.py

from django.shortcuts import render, get_object_or_404
# --- NUEVAS IMPORTACIONES ---
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Causa


def lista_causas(request):
    """
    Esta vista se encarga de obtener todas las causas de la base de datos
    y pasarlas a una plantilla para que las muestre.
    """
    todas_las_causas = Causa.objects.all().order_by('-id')
    contexto = {
        'causas': todas_las_causas,
    }
    return render(request, 'causas/lista_causas.html', contexto)


def detalle_causa(request, pk):
    """
    Esta vista obtiene una ÚNICA causa de la base de datos,
    identificada por su 'primary key' (pk) o ID.
    """
    causa_especifica = get_object_or_404(Causa, pk=pk)
    contexto = {
        'causa': causa_especifica,
    }
    return render(request, 'causas/detalle_causa.html', contexto)


# --- NUEVA VISTA BASADA EN CLASES PARA CREAR ---
class CausaCreateView(CreateView):
    model = Causa
    # Especificamos los campos que queremos que aparezcan en el formulario
    fields = ['rol', 'operacion', 'etapa_juicio', 'estado_causa', 'total_costas', 
              'arbitro', 'abogado_encargado', 'fecha_asignacion', 'deudor', 'tribunal']

    # La plantilla que usará (la crearemos en el siguiente paso)
    template_name = 'causas/causa_form.html'

    # La URL a la que se redirigirá al usuario después de crear una causa con éxito
    # reverse_lazy es la forma segura de referenciar una URL por su nombre
    success_url = reverse_lazy('lista_causas')
