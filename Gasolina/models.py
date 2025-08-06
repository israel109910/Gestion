from django.db import models

# Create your models here.
class Sitio(models.Model):
    nombre = models.CharField(max_length=100)
    distancia_km = models.DecimalField(max_digits=6, decimal_places=2)  # ida y vuelta
    requiere_tag = models.BooleanField(default=False)  # Si requiere tag del instrumento
    costo_peaje = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Costo de peaje
    seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE, related_name='sitios')

    class Meta:
        verbose_name_plural = "Viaticos - Sitios"

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Viaticos - Estados"

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='secciones')

    class Meta:
        verbose_name_plural = "Viaticos - Secciones"

    def __str__(self):
        return self.nombre

class ParametrosGlobales(models.Model):
    precio_gasolina = models.DecimalField(max_digits=5, decimal_places=2)  # Precio por litro
    rendimiento_km_l = models.DecimalField(max_digits=5, decimal_places=2)  # km/l base
    peso_herramienta = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)  # en kg
    peso_prom_persona = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)  # en kg
    factor_penalizacion = models.DecimalField(max_digits=5, decimal_places=2, default=0.5) 
    herramientas = models.BooleanField(default=False)  # Factor de penalización
    cantidad_personas = models.IntegerField(default=1)  # Cantidad de personas por sitio
    dias_trabajo = models.IntegerField(default=1)  # Días de trabajo por semana

    class Meta:
        verbose_name_plural = "Viaticos - Parámetros Globales"
        
    def __str__(self):
        return "Parámetros Globales"