from django.shortcuts import render
from django.http import HttpResponse
import json

from .models import Estado, Seccion, Sitio, ParametrosGlobales

def calcular_viaticos(request):
    estados = Estado.objects.all()
    secciones = Seccion.objects.all()
    sitios = Sitio.objects.all()
    resultado = None

    if request.method == 'POST':
        viajes_json = request.POST.get('viajes_json')
        try:
            viajes = json.loads(viajes_json)
            parametros = ParametrosGlobales.objects.first()
            resultados = []

            for viaje in viajes:
                sitio_id = viaje.get('sitio')
                personas = int(viaje.get('personas'))
                dias = int(viaje.get('dias'))
                herramientas = viaje.get('herramientas')

                sitio = Sitio.objects.get(id=sitio_id)

                km_totales = float(sitio.distancia_km)
                peso_prom_persona = float(parametros.peso_prom_persona)
                peso_herramienta = float(parametros.peso_herramienta)
                rendimiento_base = float(parametros.rendimiento_km_l)
                precio_gasolina = float(parametros.precio_gasolina)
                factor_penalizacion = float(parametros.factor_penalizacion)
                costo_peaje = float(sitio.costo_peaje) if sitio.requiere_tag else 0.0

                peso_personal = personas * peso_prom_persona
                peso_herramientas = peso_herramienta if herramientas else 0.0
                peso_total = peso_personal + peso_herramientas
                peso_relativo = peso_total / 100

                rendimiento_ajustado = rendimiento_base - (peso_relativo / factor_penalizacion)

                if rendimiento_ajustado <= 0:
                    costo_gasolina = 0
                else:
                    costo_gasolina = ((km_totales / rendimiento_ajustado) * precio_gasolina) * dias

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
                        'peso_prom_persona': peso_prom_persona,
                        'peso_herramienta': peso_herramienta if herramientas else 0.0,
                        'peso_total': round(peso_total, 2),
                        'peso_relativo': round(peso_relativo, 2),
                        'distancia_km': km_totales,
                        'rendimiento_base': rendimiento_base,
                        'rendimiento_ajustado': round(rendimiento_ajustado, 2),
                        'precio_gasolina': precio_gasolina,
                        'factor_penalizacion': factor_penalizacion,
                        'formula': "((distancia / rendimiento_ajustado) * precio_gasolina) * dias",
                        'explicacion_rendimiento': f"{rendimiento_base} - ({round(peso_relativo,2)} / {factor_penalizacion}) = {round(rendimiento_ajustado,2)}"
                    }
                })

            resultado = resultados

        except Exception as e:
            resultado = [{'error': 'Datos inválidos o incompletos.'}]

    secciones_dict = {s.id: {'nombre': s.nombre, 'estado_id': s.estado.id} for s in secciones}
    sitios_dict = {s.id: {'nombre': s.nombre, 'seccion_id': s.seccion.id} for s in sitios}

    return render(request, 'viaticos.html', {
        'estados': estados,
        'resultado': resultado,
        'secciones_json': json.dumps(secciones_dict),
        'sitios_json': json.dumps(sitios_dict),
    })
