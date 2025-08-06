from django.contrib import admin

from .models import Sitio, ParametrosGlobales, Estado, Seccion
# Register your models here.
admin.site.register(Sitio)
admin.site.register(ParametrosGlobales)     
admin.site.register(Estado) 
admin.site.register(Seccion) 