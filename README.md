# 🔀 bff_serv (Backend For Frontend)

Capa de agregación y proxy del sistema SanosYSalvos. Actúa como **punto de entrada único** para el frontend, recibiendo todas las solicitudes y redirigiéndolas al microservicio correspondiente. El frontend nunca se comunica directamente con los servicios internos.

**Puerto:** `8003`

---

## Responsabilidades

- Recibir todas las solicitudes del frontend en un único punto
- Redirigir cada solicitud al microservicio backend correspondiente
- Propagar los headers de autenticación JWT a los microservicios
- Manejar correctamente el reenvío de archivos multipart (fotos de mascotas)
- Subir fotos a imgbb y retornar la URL pública al frontend
- Retornar las respuestas de los microservicios al frontend sin modificarlas

---

## Arquitectura

```
Frontend
    │
    └── BFF (8003) ──────────────────────────────────────────┐
            │                                                │
            ├── /api/login/            → auth_serv (8001)   │
            ├── /api/refresh/          → auth_serv (8001)   │
            │                                                │
            ├── /api/usuarios/         → usuarios_serv (8000)│
            ├── /api/perfiles/         → usuarios_serv (8000)│
            ├── /api/preferencias/     → usuarios_serv (8000)│
            ├── /api/entidades/        → usuarios_serv (8000)│
            │                                                │
            ├── /api/reportes/         → mascotas_serv (8002)│
            ├── /api/contactos/        → mascotas_serv (8002)│
            │                                                │
            ├── /api/noticias/         → noticias_serv (8004)│
            │                                                │
            ├── /api/notificaciones/   → notificaciones_serv (8005)│
            │                                                │
            └── /api/upload/           → imgbb API (externo) │
```

---

## Endpoints

| Método | URL BFF | Redirige a |
|---|---|---|
| POST | `/api/login/` | `auth_serv/api/auth/login-token/` |
| POST | `/api/refresh/` | `auth_serv/api/auth/refresh/` |
| GET/POST | `/api/usuarios/` | `usuarios_serv/api/usuarios/` |
| GET/PUT/DELETE | `/api/usuarios/{id}/` | `usuarios_serv/api/usuarios/{id}/` |
| GET/POST | `/api/perfiles/` | `usuarios_serv/api/perfiles/` |
| GET/PUT/DELETE | `/api/perfiles/{id}/` | `usuarios_serv/api/perfiles/{id}/` |
| GET/POST | `/api/preferencias/` | `usuarios_serv/api/preferencias/` |
| GET/PUT/DELETE | `/api/preferencias/{id}/` | `usuarios_serv/api/preferencias/{id}/` |
| GET/POST | `/api/entidades/` | `usuarios_serv/api/entidades/` |
| GET/PUT/DELETE | `/api/entidades/{id}/` | `usuarios_serv/api/entidades/{id}/` |
| GET/POST | `/api/reportes/` | `mascotas_serv/api/reportes/` |
| GET/PUT/DELETE | `/api/reportes/{id}/` | `mascotas_serv/api/reportes/{id}/` |
| GET/POST | `/api/contactos/` | `mascotas_serv/api/contactos/` |
| GET/PUT/DELETE | `/api/contactos/{id}/` | `mascotas_serv/api/contactos/{id}/` |
| GET/POST | `/api/noticias/` | `noticias_serv/api/noticias/` |
| GET/PUT/DELETE | `/api/noticias/{id}/` | `noticias_serv/api/noticias/{id}/` |
| GET | `/api/notificaciones/usuario/` | `notificaciones_serv/api/notificaciones/usuario/` |
| GET | `/api/notificaciones/no-leidas/` | `notificaciones_serv/api/notificaciones/no-leidas/` |
| POST | `/api/notificaciones/{id}/marcar-leida/` | `notificaciones_serv/api/notificaciones/{id}/marcar-leida/` |
| POST | `/api/notificaciones/marcar-todas-leidas/` | `notificaciones_serv/api/notificaciones/marcar-todas-leidas/` |
| POST | `/api/upload/` | imgbb API externa |

> **Nota:** Se puede utilizar Thunder o Postman para las peticiones API: http://127.0.0.1:8003

---

## Endpoint de subida de fotos

El endpoint `/api/upload/` recibe una imagen del frontend, la sube a imgbb y retorna la URL pública. Es usado por el formulario de reporte antes de crear el reporte en mascotas_serv.

**Request:**
```
POST /api/upload/
Content-Type: multipart/form-data
Body: image=<archivo>
```

**Response:**
```json
{ "url": "https://i.ibb.co/xxxxx/foto.jpg" }
```

---

## Manejo de archivos multipart

El BFF detecta automáticamente si el request contiene archivos (`request.FILES`) y ajusta el reenvío:

- **Con archivos:** reenvía como `multipart/form-data` conservando el archivo y los campos del formulario
- **Sin archivos:** reenvía como JSON o form-urlencoded según corresponda

---

## Tests

Los tests usan `@patch` para simular las respuestas de los microservicios backend, verificando que el BFF proxifica correctamente sin necesitar los otros servicios corriendo.

- `test_login_bff_success` — POST login retorna token JWT (status 200)
- `test_login_bff_method_not_allowed` — GET a login retorna 405
- `test_refresh_bff_success` — POST refresh retorna nuevo token (status 200)
- `test_reportes_list_get` — GET reportes proxifica correctamente (status 200)
- `test_reportes_list_post` — POST reporte proxifica correctamente (status 201)
- `test_reportes_detail_get` — GET reporte por ID proxifica correctamente (status 200)
- `test_contactos_list_get` — GET contactos proxifica correctamente (status 200)
- `test_usuarios_list_get` — GET usuarios proxifica correctamente (status 200)
- `test_perfiles_list_get` — GET perfiles proxifica correctamente (status 200)
- `test_preferencias_list_get` — GET preferencias proxifica correctamente (status 200)

```bash
cd bff_serv
python manage.py test
```

---

## Levantar el servicio

```bash
cd bff_serv
python manage.py migrate
python manage.py runserver 8003
```

> **Nota:** Para funcionar correctamente requiere que todos los microservicios estén corriendo: `usuarios_serv` (8000), `auth_serv` (8001), `mascotas_serv` (8002), `noticias_serv` (8004) y `notificaciones_serv` (8005).