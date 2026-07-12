import json
import os
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# URL base de los microservicios que el BFF va a enrutar

#URL Microservicio de Autenticación (auth_serv)
AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL', 'http://127.0.0.1:8001/api/auth/')

#URL Microservicio de Usuarios (usuarios_serv)
USERS_SERVICE_URL = os.environ.get('USERS_SERVICE_URL', 'http://127.0.0.1:8000/api/usuarios/')
PERFILES_SERVICE_URL = os.environ.get('PERFILES_SERVICE_URL', 'http://127.0.0.1:8000/api/perfiles/')
PREFERENCIAS_SERVICE_URL = os.environ.get('PREFERENCIAS_SERVICE_URL', 'http://127.0.0.1:8000/api/preferencias/')
#URL Microservicio de Mascotas (mascotas_serv)
REPORTES_SERVICE_URL = os.environ.get('REPORTES_SERVICE_URL', 'http://127.0.0.1:8002/api/reportes/')
CONTACTOS_SERVICE_URL = os.environ.get('CONTACTOS_SERVICE_URL', 'http://127.0.0.1:8002/api/contactos/')

#URL Microservicio de Noticias (noticias_serv)
NOTICIAS_SERVICE_URL = os.environ.get('NOTICIAS_SERVICE_URL', 'http://127.0.0.1:8004/api/noticias/')

#URL Microservicio de Notificaciones (notificaciones_serv)
NOTIFICACIONES_SERVICE_URL = os.environ.get('NOTIFICACIONES_SERVICE_URL', 'http://127.0.0.1:8005/api/notificaciones/')

def _build_headers(request):
    # Construye los encabezados que se pasarán al microservicio destino.
    headers = {}
    if request.headers.get('Authorization'):
        headers['Authorization'] = request.headers['Authorization']
    return headers


def _proxy_request(method, url, request):
    # Realiza la petición HTTP hacia el servicio de backend correspondiente.
    headers = _build_headers(request)
    if request.FILES:
        files = {}
        for key, f in request.FILES.items():
                files[key] = (f.name, f.read(), f.content_type)
        data = request.POST.dict()
        response = requests.request(
            method, url,
            headers=headers,
            files=files,
            data=data,
            params=request.GET.dict() or None,
            timeout=30
        )

    else:
        data = None
        try:
            if request.body:
                try:
                    data = json.loads(request.body.decode('utf-8'))
                except (ValueError, UnicodeDecodeError):
                    data = request.body
        except Exception:
            data = request.POST.dict() or None
        response = requests.request(
            method, url,
            headers=headers,
            json=data if isinstance(data, dict) else None,
            data=None if isinstance(data, dict) else data,
            params=request.GET.dict() or None,
            timeout=10
        )



    return HttpResponse(
        response.content,
        status=response.status_code,
        content_type=response.headers.get('Content-Type', 'application/json'),
    )


@csrf_exempt
def login_bff(request):
    # Endpoint BFF para login.

    # Recibe credenciales desde el frontend y las reenvía a auth_serv.

    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request('POST', AUTH_SERVICE_URL + 'login-token/', request)


@csrf_exempt
def refresh_bff(request):
    # Endpoint BFF para refresh token.

    # Reenvía la solicitud de refresh al auth_serv.
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request('POST', AUTH_SERVICE_URL + 'refresh/', request)


@csrf_exempt
def reportes_list(request):
    # Endpoint BFF para listar o crear reportes.

    # - GET: trae la lista de reportes desde mascotas_serv
    # - POST: crea un nuevo reporte en mascotas_serv

    if request.method not in ['GET', 'POST', 'OPTIONS']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, REPORTES_SERVICE_URL, request)


@csrf_exempt
def reportes_detail(request, pk):
    # Endpoint BFF para detalle, actualización y eliminación de reportes.
    if request.method not in ['GET', 'PUT', 'DELETE']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, f'{REPORTES_SERVICE_URL}{pk}/', request)


@csrf_exempt
def usuarios_list(request):
    # Endpoint BFF para listar o crear usuarios.
    if request.method not in ['GET', 'POST', 'OPTIONS']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, USERS_SERVICE_URL, request)


@csrf_exempt
def usuarios_detail(request, pk):
    # Endpoint BFF para detalle, actualización y eliminación de usuarios.
    if request.method not in ['GET', 'HEAD', 'PUT', 'DELETE']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, f'{USERS_SERVICE_URL}{pk}/', request)


@csrf_exempt
def contactos_list(request):
    # Endpoint BFF para listar o crear contactos.
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, CONTACTOS_SERVICE_URL, request)


@csrf_exempt
def contactos_detail(request, pk):
    # Endpoint BFF para detalle, actualización y eliminación de contactos.
    if request.method not in ['GET', 'PUT', 'DELETE']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, f'{CONTACTOS_SERVICE_URL}{pk}/', request)


@csrf_exempt
def perfiles_list(request):
    # Endpoint BFF para listar o crear perfiles.
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, PERFILES_SERVICE_URL, request)


@csrf_exempt
def perfiles_detail(request, pk):
    # Endpoint BFF para detalle, actualización y eliminación de perfiles.
    if request.method not in ['GET', 'PUT', 'DELETE']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, f'{PERFILES_SERVICE_URL}{pk}/', request)


@csrf_exempt
def preferencias_list(request):
    # Endpoint BFF para listar o crear preferencias.
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, PREFERENCIAS_SERVICE_URL, request)


@csrf_exempt
def preferencias_detail(request, pk):
    # Endpoint BFF para detalle, actualización y eliminación de preferencias.
    if request.method not in ['GET', 'PUT', 'DELETE']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    return _proxy_request(request.method, f'{PREFERENCIAS_SERVICE_URL}{pk}/', request)

@csrf_exempt
def entidades_list(request):
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return _proxy_request(request.method, 'http://127.0.0.1:8000/api/entidades/', request)


@csrf_exempt
def entidades_detail(request, pk):
    if request.method not in ['GET', 'PUT', 'DELETE']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return _proxy_request(request.method, f'http://127.0.0.1:8000/api/entidades/{pk}/', request)

@csrf_exempt
def noticias_list(request):
    if request.method not in ['GET', 'POST']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return _proxy_request(request.method, NOTICIAS_SERVICE_URL, request)

@csrf_exempt
def noticias_detail(request, pk):
    if request.method not in ['GET', 'PUT', 'DELETE']:
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return _proxy_request(request.method, f'{NOTICIAS_SERVICE_URL}{pk}/', request)


csrf_exempt
def notificaciones_usuario(request):

    # GET /bff/notificaciones/usuario/?usuario_id=1
    # Lista las notificaciones del usuario — para mostrarlas en el frontend.

    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return _proxy_request('GET', NOTIFICACIONES_SERVICE_URL + 'usuario/', request)
 
 
@csrf_exempt
def notificaciones_no_leidas(request):

    # GET /bff/notificaciones/no-leidas/?usuario_id=1
    # Conteo de no leídas — para el badge del ícono de notificaciones.

    if request.method != 'GET':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return _proxy_request('GET', NOTIFICACIONES_SERVICE_URL + 'no-leidas/', request)
 
 
@csrf_exempt
def notificaciones_marcar_leida(request, pk):

    # POST /bff/notificaciones/<id>/marcar-leida/
    # Marca una notificación como leída cuando el usuario la abre.

    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return _proxy_request('POST', f'{NOTIFICACIONES_SERVICE_URL}{pk}/marcar-leida/', request)
    
 
@csrf_exempt
def notificaciones_marcar_todas_leidas(request):

    # POST /bff/notificaciones/marcar-todas-leidas/
    # Marca todas las notificaciones del usuario como leídas.

    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    return _proxy_request('POST', NOTIFICACIONES_SERVICE_URL + 'marcar-todas-leidas/', request)



# Endpoint para subir fotos a imgbb (usado por el frontend al crear reportes)
@csrf_exempt
def upload_foto(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image provided'}, status=400)
    
    file = request.FILES['image']
    IMGBB_API_KEY = 'a8b8d63944d3b3c0c4e2aff5fdcc6403'
    
    try:
        response = requests.post(
            'https://api.imgbb.com/1/upload',
            params={'key': IMGBB_API_KEY},
            files={'image': (file.name, file.read(), file.content_type)},
            timeout=30
        )
        data = response.json()
        if data.get('success'):
            return JsonResponse({'url': data['data']['url']})
        return JsonResponse({'error': 'Upload failed'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)