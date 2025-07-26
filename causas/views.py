# causas/views.py
from django import forms
from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Causa, Cartera
from .forms import ArchivoAdjuntoForm, ComentarioForm, EtapaCausaForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

@login_required
def dashboard_view(request):
    """
    Esta vista calcula las métricas principales (KPIs) y prepara los datos para el gráfico.
    """
    # Los cálculos que ya teníamos se mantienen
    total_causas = Causa.objects.count()
    activos = Causa.objects.filter(estado_causa='ACTIVO').count()
    recuperados = Causa.objects.filter(estado_causa='RECUPERADO').count()
    suspendidos = Causa.objects.filter(estado_causa='SUSPENDIDO').count()
    archivados = Causa.objects.filter(estado_causa='ARCHIVADO').count()

    # --- NUEVO CÓDIGO PARA EL GRÁFICO ---
    # Preparamos las etiquetas (los nombres de cada "quesito" del pastel)
    chart_labels = ['Activas', 'Recuperadas', 'Suspendidas', 'Archivadas']
    # Preparamos los datos (los números de cada "quesito")
    chart_data = [activos, recuperados, suspendidos, archivados]

    # Preparamos el contexto para enviarlo a la plantilla
    contexto = {
        'total_causas': total_causas,
        'causas_activas': activos,
        'causas_recuperadas': recuperados,
        'causas_suspendidas': suspendidos,
        'causas_archivadas': archivados,
        
        # Añadimos los nuevos datos del gráfico al contexto
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }

    # Renderizamos la plantilla del dashboard
    return render(request, 'causas/dashboard.html', contexto)

@login_required
def lista_causas(request):
    # Obtenemos los posibles filtros de la URL
    estado_filtro = request.GET.get('estado', None)
    cartera_filtro_id = request.GET.get('cartera_id', None)

    # Empezamos con todas las causas
    listado = Causa.objects.all()
    # 1. Inicializamos una variable para la cartera activa
    cartera_activa = None

    # Aplicamos el filtro de estado si existe
    if estado_filtro:
        listado = listado.filter(estado_causa=estado_filtro)

    # Aplicamos el filtro de cartera si existe
    if cartera_filtro_id:
        listado = listado.filter(cartera__id=cartera_filtro_id)
        # 2. Si filtramos, obtenemos el objeto Cartera para saber su nombre
        try:
            cartera_activa = Cartera.objects.get(id=cartera_filtro_id)
        except Cartera.DoesNotExist:
            cartera_activa = None # Por si alguien pone un ID que no existe en la URL

    # Ordenamos el resultado final
    listado_ordenado = listado.order_by('-id')

    # 3. Añadimos la cartera_activa al contexto que enviamos a la plantilla
    contexto = {
        'causas': listado_ordenado,
        'cartera_activa': cartera_activa,
    }
    return render(request, 'causas/lista_causas.html', contexto)

# causas/views.py

@login_required
def detalle_causa(request, pk):
    causa_especifica = get_object_or_404(Causa, pk=pk)
    
    # Identificamos el formulario que se está enviando
    if request.method == 'POST':
        if 'submit_etapa' in request.POST:
            etapa_form = EtapaCausaForm(request.POST)
            if etapa_form.is_valid():
                new_etapa = etapa_form.save(commit=False)
                new_etapa.causa = causa_especifica
                new_etapa.save()
                return redirect('detalle_causa', pk=pk)
        
        elif 'submit_comentario' in request.POST:
            comment_form = ComentarioForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.causa = causa_especifica
                new_comment.autor = request.user
                new_comment.save()
                return redirect('detalle_causa', pk=pk)
        
        elif 'submit_adjunto' in request.POST:
            attachment_form = ArchivoAdjuntoForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment_form.save()
                return redirect('detalle_causa', pk=pk)

    # Si es una petición GET, mostramos los formularios vacíos
    etapa_form = EtapaCausaForm()
    comment_form = ComentarioForm()
    attachment_form = ArchivoAdjuntoForm()

    contexto = {
        'causa': causa_especifica,
        'comment_form': comment_form,
        'etapa_form': etapa_form,
        'attachment_form': attachment_form,
    }
    return render(request, 'causas/detalle_causa.html', contexto)


class CausaCreateView(CreateView):
    permission_required = 'causas.add_causa'
    model = Causa
    fields = ['rol', 'operacion', 'estado_causa', 'total_costas', 
              'arbitro', 'abogado_encargado', 'fecha_asignacion', 'deudor', 'tribunal', 'cartera']
    template_name = 'causas/causa_form.html'
    success_url = reverse_lazy('lista_causas')

    def get_initial(self):
        """
        Este método establece los valores iniciales del formulario.
        """
        initial = super().get_initial()
        # 1. Leemos el cartera_id de la URL.
        cartera_id = self.request.GET.get('cartera_id')
        if cartera_id:
            # 2. Si existe, lo ponemos como valor inicial para el campo 'cartera'.
            initial['cartera'] = cartera_id
        return initial

    def get_form(self, form_class=None):
        """
        Este método nos permite modificar el formulario antes de mostrarlo.
        """
        form = super().get_form(form_class)
        # 3. Si venimos con un cartera_id en la URL...
        if self.request.GET.get('cartera_id'):
            # 4. ...entonces ocultamos el campo 'cartera' del formulario.
            if 'cartera' in form.fields:
                form.fields['cartera'].widget = forms.HiddenInput()
        return form

class CausaUpdateView(UpdateView):
    model = Causa
    fields = ['rol', 'operacion', 'estado_causa', 'total_costas', 
              'arbitro', 'abogado_encargado', 'fecha_asignacion', 'deudor', 'tribunal', 'cartera']
    template_name = 'causas/causa_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos el formulario de archivos adjuntos al contexto
        context['attachment_form'] = ArchivoAdjuntoForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Identificamos qué botón se presionó
        if 'update_causa' in request.POST:
            # Si se presionó el botón de editar causa, procesamos ese formulario
            form = self.get_form()
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                # Si el formulario no es válido, lo volvemos a mostrar con errores
                return self.render_to_response(self.get_context_data(form=form))
        
        elif 'upload_attachment' in request.POST:
            # Si se presionó el botón de subir archivo, procesamos ese formulario
            form = self.get_form() # Necesitamos el form principal para el contexto
            attachment_form = ArchivoAdjuntoForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.causa = self.object # Asignamos la causa actual
                attachment.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                # Si el formulario de adjuntos no es válido, lo mostramos con errores
                return self.render_to_response(
                    self.get_context_data(form=form, attachment_form=attachment_form)
                )

        # Por si acaso, si la petición no viene de ninguno de los botones
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('editar_causa', kwargs={'pk': self.object.pk})

class CausaDeleteView(DeleteView):
    model = Causa
    
    # Django por defecto buscará una plantilla llamada 'nombredelmodelo_confirm_delete.html'
    # En nuestro caso, buscará 'causa_confirm_delete.html'.
    # No es necesario especificar el template_name si seguimos esta convención.
    
    # La URL a la que se redirigirá al usuario después de eliminar con éxito.
    success_url = reverse_lazy('lista_causas')