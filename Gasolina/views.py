# Gasolina/views.py

from django.shortcuts import render
from django.http import HttpResponse
import json

from .models import Estado, Seccion, Sitio, ParametrosGlobales

def calcular_viaticos(request):
    estados = Estado.objects.all()
    secciones = Seccion.objects.all()
    sitios = Sitio.objects.all()
    resultados = []

    if request.method == 'POST':
        viajes_json = request.POST.get('viajes_json')
        try:
            viajes = json.loads(viajes_json)
            parametros = ParametrosGlobales.objects.first()
            for viaje in viajes:
                sitio_id = viaje.get('sitio')
                personas = int(viaje.get('personas'))
                dias = int(viaje.get('dias'))
                herramientas = viaje.get('herramientas')

                sitio = Sitio.objects.get(id=sitio_id)
                km_totales = float(sitio.distancia_km)
                peso_personal = personas * float(parametros.peso_prom_persona)
                peso_herramientas = float(parametros.peso_herramienta) if herramientas else 0.0
                peso_total = peso_personal + peso_herramientas
                peso_relativo = peso_total / 100

                rendimiento_ajustado = float(parametros.rendimiento_km_l) - (peso_relativo / float(parametros.factor_penalizacion))
                costo_peaje = float(sitio.costo_peaje) if sitio.requiere_tag else 0.0
                costo_gasolina = 0 if rendimiento_ajustado <= 0 else ((km_totales / rendimiento_ajustado) * float(parametros.precio_gasolina)) * dias

                resultados.append({
                    'sitio': sitio.nombre,
                    'requiere_tag': sitio.requiere_tag,
                    'costo_peaje': costo_peaje,
                    'costo_gasolina': round(costo_gasolina, 2),
                    'costo_total': round(costo_gasolina + costo_peaje, 2),
                    'detalle': {
                        'personas': personas,
                        'dias': dias,
                        'herramientas': herramientas,
                        'peso_total': round(peso_total, 2),
                        'rendimiento_ajustado': round(rendimiento_ajustado, 2),
                        'formula': f"((km_totales / rendimiento_ajustado) * precio_gas) * dias"
                    }
                })
        except Exception as e:
            resultados.append({'error': 'Datos inválidos o incompletos.'})

    return render(request, 'viaticos.html', {
        'estados': estados,
        'resultado': resultados,
        'secciones_json': json.dumps({s.id: {'nombre': s.nombre, 'estado_id': s.estado.id} for s in secciones}),
        'sitios_json': json.dumps({s.id: {'nombre': s.nombre, 'seccion_id': s.seccion.id} for s in sitios}),
    })