# Importamos el User de Django para los abogados y otras herramientas
from django.db import models
from django.conf import settings # Para referenciar al modelo User

# --- Modelo 1: Tribunal ---
class Tribunal(models.Model):
    nombre = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nombre

# --- Modelo 2: Deudor ---
class Deudor(models.Model):
    nombres = models.CharField(max_length=150, verbose_name="Nombres del Deudor")
    apellidos = models.CharField(max_length=150, verbose_name="Apellidos del Deudor")
    rut = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

# --- Modelo 3: Causa (El Modelo Principal y Completo) ---
class Causa(models.Model):
    # Opciones predefinidas para los campos de elección
    class EtapaJuicio(models.TextChoices):
        LANZAMIENTO = 'LANZAMIENTO', 'Lanzamiento'
        VIVIENDA_RECUPERADA = 'RECUPERADA', 'Vivienda recuperada'
        # ... puedes añadir todas las demás etapas aquí
    
    class EstadoCausa(models.TextChoices):
        RECUPERADO = 'RECUPERADO', 'Recuperado'
        ACTIVO = 'ACTIVO', 'Activo'
        # ... puedes añadir todos los demás estados aquí

    # --- CAMPOS DE TU IMAGEN ---
    
    # Datos de la Causa
    rol = models.CharField(max_length=50, unique=True, verbose_name="Rol")
    operacion = models.CharField(max_length=100, blank=True, verbose_name="Operación")
    etapa_juicio = models.CharField(max_length=50, choices=EtapaJuicio.choices, verbose_name="Etapa del Juicio")
    total_costas = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Total Costas")
    estado_causa = models.CharField(max_length=50, choices=EstadoCausa.choices, verbose_name="Estado de la Causa")
    arbitro = models.CharField(max_length=200, blank=True, verbose_name="Árbitro")
    
    # Asignación y Fechas
    # Usamos el modelo User que viene con Django para representar a los abogados
    abogado_encargado = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Abogado Encargado"
    )
    fecha_asignacion = models.DateField(null=True, blank=True, verbose_name="Fecha de Asignación")

    # --- RELACIONES (Foreign Keys) ---
    deudor = models.ForeignKey(Deudor, on_delete=models.CASCADE, verbose_name="Deudor Asociado")
    tribunal = models.ForeignKey(Tribunal, on_delete=models.SET_NULL, null=True, verbose_name="Tribunal")

    def __str__(self):
        return self.rol
