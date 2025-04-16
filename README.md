# API de Compras con FastAPI

Una API REST basada en FastAPI para la gestión de compras con autenticación de usuarios y control de acceso basado en roles.

## Características

- Autenticación de usuarios con JWT
- Control de acceso basado en roles (Administrador, Supervisor, Usuario)
- Base de datos SQL Server con SQLAlchemy ORM
- Migraciones de base de datos con Alembic
- Gestión de solicitudes de compra
- Seguimiento del estado de las solicitudes
- Sistema de comentarios para solicitudes
- Registro de auditoría de cambios
- Generación de reportes en CSV
- Estructura de proyecto modular
- Contenedorización con Docker

## Requisitos Previos

- Python 3.8+
- SQL Server
- pip (gestor de paquetes de Python)
- Docker y Docker Compose (opcional)

## Instalación

### Método Tradicional

1. Clonar el repositorio:
```bash
git clone https://github.com/ifbriceno1996br/back-api-web-purchase.git
cd WebApiPurchase
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
- Crear una base de datos en SQL Server
- Actualizar la configuración de conexión en `app/core/config.py` si es necesario

5. Ejecutar migraciones de la base de datos:
```bash
alembic upgrade head
```

### Método con Docker

1. Clonar el repositorio:
```bash
git clone https://github.com/ifbriceno1996br/back-api-web-purchase.git
cd WebApiPurchase
```

2. Construir las imágenes:
```bash
docker-compose build
```

3. Iniciar los contenedores:
```bash
docker-compose up -d
```

4. Ver los logs:
```bash
docker-compose logs -f
```

## Ejecución de la Aplicación

### Método Tradicional
```bash
uvicorn app.main:app --reload
```

### Método con Docker
La aplicación ya estará ejecutándose después de `docker-compose up -d`

La API estará disponible en `http://localhost:8000`

## Documentación de la API

Una vez que el servidor esté en ejecución, puedes acceder a:
- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

## Estructura del Proyecto

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── users.py
│   │   │   ├── roles.py
│   │   │   ├── requests.py
│   │   │   ├── comments.py
│   │   │   └── audits.py
│   │   └── api.py
│   └── deps.py
├── core/
│   ├── config.py
│   └── security.py
├── crud/
│   ├── crud_user.py
│   ├── crud_role.py
│   └── crud_request.py
├── db/
│   ├── base_class.py
│   └── session.py
├── models/
│   ├── user.py
│   ├── role.py
│   ├── request.py
│   ├── comment.py
│   └── audit.py
├── schemas/
│   ├── user.py
│   ├── role.py
│   └── request.py
└── main.py
```

## Endpoints de la API

### Autenticación
- POST /api/v1/login/access-token - Iniciar sesión y obtener token de acceso
- POST /api/v1/login/test-token - Probar token de acceso

### Usuarios
- POST /api/v1/users/ - Crear un nuevo usuario
- GET /api/v1/users/ - Obtener todos los usuarios
- GET /api/v1/users/{user_id} - Obtener un usuario específico
- PUT /api/v1/users/{user_id} - Actualizar un usuario
- DELETE /api/v1/users/{user_id} - Eliminar un usuario

### Roles
- POST /api/v1/roles/ - Crear un nuevo rol
- GET /api/v1/roles/ - Obtener todos los roles
- GET /api/v1/roles/{role_id} - Obtener un rol específico
- PUT /api/v1/roles/{role_id} - Actualizar un rol
- DELETE /api/v1/roles/{role_id} - Eliminar un rol

### Solicitudes
- POST /api/v1/requests/ - Crear una nueva solicitud
- GET /api/v1/requests/ - Obtener todas las solicitudes (filtradas por usuario/supervisor)
- GET /api/v1/requests/{request_id} - Obtener una solicitud específica
- PUT /api/v1/requests/{request_id} - Actualizar una solicitud
- PUT /api/v1/requests/{request_id}/status - Cambiar estado de la solicitud (solo supervisores)
- DELETE /api/v1/requests/{request_id} - Eliminar una solicitud
- GET /api/v1/requests/report/csv - Descargar reporte de solicitudes en formato CSV

### Comentarios
- POST /api/v1/comments/ - Crear un nuevo comentario
- GET /api/v1/comments/ - Obtener todos los comentarios
- GET /api/v1/comments/{comment_id} - Obtener un comentario específico
- PUT /api/v1/comments/{comment_id} - Actualizar un comentario
- DELETE /api/v1/comments/{comment_id} - Eliminar un comentario

### Auditoría
- GET /api/v1/audits/ - Obtener todos los registros de auditoría
- GET /api/v1/audits/{audit_id} - Obtener un registro de auditoría específico

## Flujo de Estados de las Solicitudes

1. **Creado** - Estado inicial cuando se crea una solicitud
2. **Pendiente** - La solicitud está esperando revisión del supervisor
3. **Aprobado** - La solicitud ha sido aprobada por el supervisor
4. **Rechazado** - La solicitud ha sido rechazada por el supervisor
5. **Completado** - La solicitud ha sido cumplida

## Permisos por Rol

- **Administrador**: Acceso completo a todos los endpoints
- **Supervisor**: Puede aprobar/rechazar solicitudes, ver todas las solicitudes y generar reportes
- **Usuario**: Puede crear y ver sus propias solicitudes

## Generación de Reportes

La API proporciona una función de generación de reportes en CSV que incluye:
- Detalles de la solicitud
- Información del usuario
- Historial de estados
- Comentarios
- Registro de auditoría
- Métricas (días desde la creación, días hasta la fecha esperada)

Los reportes se pueden filtrar por:
- Rango de fechas
- Estado
- ID de usuario

## Configuración de Docker

El proyecto incluye configuración para Docker y Docker Compose:

### Archivos de Configuración
- `Dockerfile`: Configuración del contenedor de la aplicación
- `docker-compose.yml`: Configuración de los servicios (aplicación y base de datos)
- `.env`: Variables de entorno para la configuración

### Comandos Útiles
```bash
# Construir las imágenes
docker-compose build

# Iniciar los contenedores
docker-compose up -d

# Detener los contenedores
docker-compose down

# Ver los logs
docker-compose logs -f

# Reconstruir las imágenes
docker-compose up --build
```

### Notas Importantes
- La base de datos SQL Server se ejecuta en un contenedor separado
- Los datos de la base de datos persisten en un volumen de Docker
- La aplicación se reinicia automáticamente cuando se detectan cambios en el código
- Las variables de entorno se pueden configurar en el archivo `.env`

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. 