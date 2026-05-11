import json
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# URL base de los microservicios que el BFF va a enrutar

#URL Microservicio de Autenticación (auth_serv)
AUTH_SERVICE_URL = "http://127.0.0.1:8001/api/auth/"

#URL Microservicio de Usuarios (usuarios_serv)
USERS_SERVICE_URL = "http://127.0.0.1:8000/api/usuarios/"
PERFILES_SERVICE_URL = "http://127.0.0.1:8000/api/perfiles/"
PREFERENCIAS_SERVICE_URL = "http://127.0.0.1:8000/api/preferencias/"

#URL Microservicio de Mascotas (mascotas_serv)
REPORTES_SERVICE_URL = "http://127.0.0.1:8002/api/reportes/"
CONTACTOS_SERVICE_URL = "http://127.0.0.1:8002/api/contactos/"


def _build_headers(request):
    # Construye los encabezados que se pasarán al microservicio destino.
    headers = {}
    if request.headers.get('Authorization'):
        headers['Authorization'] = request.headers['Authorization']
    if request.content_type:
        headers['Content-Type'] = request.content_type
    return headers


def _proxy_request(method, url, request):
    # Realiza la petición HTTP hacia el servicio de backend correspondiente.
    headers = _build_headers(request)

    data = None
    if request.body:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            data = request.body

    response = requests.request(
        method,
        url,
        headers=headers,
        json=data if isinstance(data, dict) else None,
        data=None if isinstance(data, dict) else data,
        params=request.GET.dict() if request.GET else None,
        timeout=10,
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
