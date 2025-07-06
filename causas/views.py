# causas/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

class CausaUpdateView(UpdateView):
    model = Causa
    # Usamos los mismos campos que en el formulario de creación
    fields = ['rol', 'operacion', 'etapa_juicio', 'estado_causa', 'total_costas', 
            'arbitro', 'abogado_encargado', 'fecha_asignacion', 'deudor', 'tribunal']
    
    # ¡Reutilizamos la misma plantilla del formulario de creación!
    template_name = 'causas/causa_form.html'
    
    # En lugar de un success_url fijo, definimos un método para
    # que después de editar, nos redirija a la página de detalle de ESA misma causa.
    def get_success_url(self):
        return reverse_lazy('detalle_causa', kwargs={'pk': self.object.pk})

class CausaDeleteView(DeleteView):
    model = Causa
    
    # Django por defecto buscará una plantilla llamada 'nombredelmodelo_confirm_delete.html'
    # En nuestro caso, buscará 'causa_confirm_delete.html'.
    # No es necesario especificar el template_name si seguimos esta convención.
    
    # La URL a la que se redirigirá al usuario después de eliminar con éxito.
    success_url = reverse_lazy('lista_causas')