from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from unittest.mock import patch, MagicMock
from .views import (
    login_bff, refresh_bff, reportes_list, reportes_detail,
    contactos_list, contactos_detail, usuarios_list, usuarios_detail,
    perfiles_list, perfiles_detail, preferencias_list, preferencias_detail
)


class BFFProxyTest(TestCase):
    # Tests de la capa BFF que proxifica solicitudes a los microservicios backend
    def setUp(self):
        self.factory = RequestFactory()

    # Verifica que el login sea procesado correctamente devolviendo tokens JWT
    @patch('bff_app.views.requests.request')
    def test_login_bff_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"access": "token123", "refresh": "refresh123"}'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.post('/api/login/')
        response = login_bff(request)
        self.assertEqual(response.status_code, 200)

    # Verifica que GET al endpoint de login retorna error 405 (método no permitido)
    @patch('bff_app.views.requests.request')
    def test_login_bff_method_not_allowed(self, mock_request):
        request = self.factory.get('/api/login/')
        response = login_bff(request)
        self.assertEqual(response.status_code, 405)

    # Verifica que el refresh de token funciona correctamente generando un nuevo token
    @patch('bff_app.views.requests.request')
    def test_refresh_bff_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"access": "newtoken"}'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.post('/api/refresh/')
        response = refresh_bff(request)
        self.assertEqual(response.status_code, 200)

    # Obtiene lista de reportes desde el BFF (proxifica a mascotas_serv)
    @patch('bff_app.views.requests.request')
    def test_reportes_list_get(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1, "titulo": "Test"}]'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.get('/api/reportes/')
        response = reportes_list(request)
        self.assertEqual(response.status_code, 200)

    # Crea un nuevo reporte a través del BFF (proxifica POST a mascotas_serv)
    @patch('bff_app.views.requests.request')
    def test_reportes_list_post(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b'{"id": 2, "titulo": "New Report"}'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.post('/api/reportes/', {'titulo': 'New Report'})
        response = reportes_list(request)
        self.assertEqual(response.status_code, 201)

    # Obtiene los detalles de un reporte específico por ID
    @patch('bff_app.views.requests.request')
    def test_reportes_detail_get(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"id": 1, "titulo": "Test"}'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.get('/api/reportes/1/')
        response = reportes_detail(request, pk=1)
        self.assertEqual(response.status_code, 200)

    # Obtiene lista de contactos asociados a los reportes
    @patch('bff_app.views.requests.request')
    def test_contactos_list_get(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1, "nombre": "Test"}]'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.get('/api/contactos/')
        response = contactos_list(request)
        self.assertEqual(response.status_code, 200)

    # Obtiene lista de usuarios del sistema (proxifica a usuarios_serv)
    @patch('bff_app.views.requests.request')
    def test_usuarios_list_get(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1, "nombre": "Test"}]'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.get('/api/usuarios/')
        response = usuarios_list(request)
        self.assertEqual(response.status_code, 200)

    # Obtiene lista de perfiles de entidades de los usuarios
    @patch('bff_app.views.requests.request')
    def test_perfiles_list_get(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1, "nombre_entidad": "Test"}]'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.get('/api/perfiles/')
        response = perfiles_list(request)
        self.assertEqual(response.status_code, 200)

    # Obtiene las preferencias de notificación de los usuarios
    @patch('bff_app.views.requests.request')
    def test_preferencias_list_get(self, mock_request):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1, "notificaciones_email": true}]'
        mock_response.headers = {'Content-Type': 'application/json'}
        mock_request.return_value = mock_response

        request = self.factory.get('/api/preferencias/')
        response = preferencias_list(request)
        self.assertEqual(response.status_code, 200)
