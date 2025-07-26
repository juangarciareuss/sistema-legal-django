# causas/models.py

from django.db import models
from django.conf import settings # Para referenciar al modelo User de Django

# --- MODELOS DE CATEGORIZACIÓN ---
class TipoEtapa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre

class Etapa(models.Model):
    tipo_etapa = models.ForeignKey(TipoEtapa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.tipo_etapa.nombre} - {self.nombre}"

# Modelo para las Carteras de Clientes
class Cartera(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para los Tribunales
class Tribunal(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre

# Modelo para los Deudores
class Deudor(models.Model):
    nombres = models.CharField(max_length=150, verbose_name="Nombres del Deudor")
    apellidos = models.CharField(max_length=150, verbose_name="Apellidos del Deudor")
    rut = models.CharField(max_length=12, unique=True, help_text="RUT sin puntos y con guión")
    direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección")
    comuna = models.CharField(max_length=100, blank=True, verbose_name="Comuna")

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class Causa(models.Model):
    class EstadoCausa(models.TextChoices):
        RECUPERADO = 'RECUPERADO', 'Recuperado'
        ACTIVO = 'ACTIVO', 'Activo'
        SUSPENDIDO = 'SUSPENDIDO', 'Suspendido'
        ARCHIVADO = 'ARCHIVADO', 'Archivado'
    
    # ... (todos los campos de Causa, excepto etapa_juicio)
    deudor = models.ForeignKey(Deudor, on_delete=models.CASCADE, verbose_name="Deudor Asociado")
    tribunal = models.ForeignKey(Tribunal, on_delete=models.SET_NULL, null=True, verbose_name="Tribunal")
    cartera = models.ForeignKey(Cartera, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Cartera de Cliente")
    abogado_encargado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Abogado Encargado")
    rol = models.CharField(max_length=50, unique=True, verbose_name="Rol Civil")
    operacion = models.CharField(max_length=100, blank=True, verbose_name="Operación")
    estado_causa = models.CharField(max_length=50, choices=EstadoCausa.choices, verbose_name="Estado de la Causa")
    arbitro = models.CharField(max_length=200, blank=True, verbose_name="Juez Árbitro")
    total_costas = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Total Costas")
    demandante = models.CharField(max_length=200, blank=True, verbose_name="Demandante")
    ubicacion_expediente = models.CharField(max_length=100, blank=True, verbose_name="Ubicación Expediente")
    rol_juez_arbitro = models.CharField(max_length=50, blank=True, verbose_name="Rol Juez Árbitro")
    rol_exhorto = models.CharField(max_length=50, blank=True, verbose_name="Rol Exhorto")
    tribunal_exhorto = models.CharField(max_length=200, blank=True, verbose_name="Tribunal Exhorto")
    n_dividendo_moroso = models.IntegerField(null=True, blank=True, verbose_name="Nº Dividendo Moroso")
    mes_ano_cuota_morosa = models.CharField(max_length=50, blank=True, verbose_name="Mes y Año Cuota Morosa")
    fecha_asignacion = models.DateField(null=True, blank=True, verbose_name="Fecha de Asignación")
    fecha_estado = models.DateField(null=True, blank=True, verbose_name="Fecha Estado")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso al Sistema")
    ultima_actualizacion = models.DateField(auto_now=True, verbose_name="Última Actualización")

    @property
    def etapa_actual(self):
        """Devuelve la etapa más reciente registrada en el historial."""
        ultimo_registro = self.etapas.order_by('-fecha').first()
        if ultimo_registro:
            return ultimo_registro.etapa.nombre
        return "Sin Etapas Registradas"

    def __str__(self):  
        return self.rol

class EtapaCausa(models.Model):
    causa = models.ForeignKey(Causa, on_delete=models.CASCADE, related_name='etapas')
    etapa = models.ForeignKey(Etapa, on_delete=models.PROTECT)
    fecha = models.DateField()
    descripcion = models.TextField(blank=True)
    costas = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    
    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.etapa.nombre} - {self.causa.rol}"


class ArchivoAdjunto(models.Model):
    # Ahora un archivo se asocia a un evento específico en el historial
    etapa_causa = models.ForeignKey(EtapaCausa, on_delete=models.CASCADE, related_name='archivos', null=True, blank=True)
    archivo = models.FileField(upload_to='adjuntos_causas/')
    descripcion = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"Archivo para {self.etapa_causa}"
    
class Comentario(models.Model):
    causa = models.ForeignKey('Causa', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion'] # Ordenar del más nuevo al más antiguo

    def __str__(self):
        return f'Comentario de {self.autor} en {self.causa.rol}'
    

class AntecedentesLeasing(models.Model):
    causa = models.OneToOneField('Causa', on_delete=models.CASCADE, primary_key=True)
    repertorio = models.CharField(max_length=100, blank=True)
    nombre_notaria = models.CharField(max_length=200, blank=True, verbose_name="Nombre Notaría")
    comuna_notaria = models.CharField(max_length=100, blank=True, verbose_name="Comuna Notaría")
    fecha_escritura = models.DateField(null=True, blank=True, verbose_name="Fecha Escritura")
    nacionalidad = models.CharField(max_length=100, blank=True)
    estado_civil = models.CharField(max_length=100, blank=True)
    ocupacion = models.CharField(max_length=100, blank=True, verbose_name="Ocupación")
    precio_compraventa_uf = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio Compraventa UF")
    aporte_mensual_uf = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name="Aporte Mensual UF")
    fecha_primera_cuota = models.CharField(max_length=100, blank=True, verbose_name="Fecha Primera Cuota")
    plazo_arriendo = models.IntegerField(null=True, blank=True, verbose_name="Plazo Arriendo (meses)")
    clausula_penal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Cláusula Penal")
    ubicacion_clausula_penal = models.CharField(max_length=200, blank=True, verbose_name="Ubicación Cláusula Penal")
    
    def __str__(self):
        return f"Antecedentes Leasing para Causa {self.causa.rol}"
    
class AntecedentesCBR(models.Model):
    causa = models.OneToOneField('Causa', on_delete=models.CASCADE, primary_key=True)
    direccion_vivienda_cbr = models.TextField(blank=True, verbose_name="Dirección Vivienda CBR")
    comuna_cbr = models.CharField(max_length=100, blank=True, verbose_name="Comuna CBR")
    fojas_dominio = models.CharField(max_length=100, blank=True, verbose_name="Fojas Dominio")
    numero_dominio = models.CharField(max_length=100, blank=True, verbose_name="Número Dominio")
    ano_dominio = models.CharField(max_length=4, blank=True, verbose_name="Año Dominio")
    fojas_arriendo = models.CharField(max_length=100, blank=True, verbose_name="Fojas Arriendo")
    numero_arriendo = models.CharField(max_length=100, blank=True, verbose_name="Número Arriendo")
    ano_arriendo = models.CharField(max_length=4, blank=True, verbose_name="Año Arriendo")
    repertorio_cesion = models.CharField(max_length=100, blank=True, verbose_name="Repertorio Cesión")
    nombre_notaria_cesion = models.CharField(max_length=200, blank=True, verbose_name="Nombre Notaría Cesión")
    comuna_notaria_cesion = models.CharField(max_length=100, blank=True, verbose_name="Comuna Notaría Cesión")
    fecha_escritura_cesion = models.DateField(null=True, blank=True, verbose_name="Fecha Escritura Cesión")

    def __str__(self):
        return f"Antecedentes CBR para Causa {self.causa.rol}"