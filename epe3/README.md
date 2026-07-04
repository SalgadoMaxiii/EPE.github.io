# Sistema de Ventas para Cuadros

## Ficha técnica
- Nombre: Sistema de ventas para cuadros
- Descripción: Aplicación web para gestionar ventas de un negocio de cuadros, con registro de usuarios, verificación por correo, recuperación de contraseña y panel de estadísticas de ventas.
- Tecnologías:
  - Django 5.1.3
  - SQLite (por defecto) / MySQL opcional
  - Bootstrap 5 para interfaz
  - Chart.js para gráficos
- Funcionalidades principales:
  - Registro de usuarios con activación por correo
  - Inicio de sesión y cierre de sesión
  - Recuperación de contraseña vía email
  - Registro y listado de ventas
  - Panel con estadísticas: ventas del día, mes y año
  - Gráfico de ventas diarias
- Autor: Implementado en el proyecto `epe3`

## Requisitos
- Python 3.11
- pip
- MySQL (opcional, solo si se usa `DB_ENGINE=mysql`)

## Instalación y configuración
1. Clonar o copiar el proyecto en tu equipo.
2. Crear un entorno virtual recomendado:
   - `python -m venv .venv`
   - `.
\venv\Scripts\Activate.ps1` (Windows PowerShell)
3. Instalar dependencias:
   - `python -m pip install -r requirements.txt`
4. Configurar variables de entorno en `.env`:
   - `SECRET_KEY`
   - `DB_ENGINE` (opcional: `sqlite3` o `mysql`)
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
   - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_HOST`, `EMAIL_PORT`
5. Ejecutar migraciones:
   - `python manage.py migrate`
6. Crear un superusuario (opcional):
   - `python manage.py createsuperuser`
7. Arrancar el servidor:
   - `python manage.py runserver`

## Despliegue en producción
Para publicar la aplicación en la web, sigue estos pasos básicos:

1. Configura un servicio de hosting compatible con Django, por ejemplo:
   - Heroku
   - PythonAnywhere
   - Render
   - Vercel (con soporte Django)
   - cualquier servidor Linux con `gunicorn` y Nginx.
2. Asegúrate de tener `DEBUG=False` en producción y `ALLOWED_HOSTS` con tu dominio.
3. Ejecuta `python manage.py collectstatic` para recopilar archivos estáticos.
4. Usa `gunicorn` como servidor de aplicaciones:
   - `gunicorn sales_gallery.wsgi:application`
5. Configura el host web (Nginx o el propio servicio) para servir `STATIC_ROOT`.

## Variables de entorno
- `SECRET_KEY`: clave secreta de Django.
- `DB_ENGINE`: `sqlite3` por defecto o `mysql` para MySQL.
- `DB_NAME`: nombre de la base de datos.
- `DB_USER`: usuario de la base de datos.
- `DB_PASSWORD`: contraseña de la base de datos.
- `DB_HOST`: host de la base de datos.
- `DB_PORT`: puerto de la base de datos.
- `EMAIL_HOST_USER`: usuario SMTP para envíos de correo.
- `EMAIL_HOST_PASSWORD`: contraseña SMTP.
- `EMAIL_HOST`: servidor SMTP (por ejemplo, `smtp.gmail.com`).
- `EMAIL_PORT`: puerto SMTP (por ejemplo, `587`).

## Uso
- Abrir la aplicación en `http://localhost:8000/`
- Crear cuenta y activar desde el enlace enviado por correo o mostrado en consola
- Iniciar sesión para acceder al panel de ventas
- Registrar ventas en el apartado "Registrar venta"
- Revisar el historial y las estadísticas en el dashboard

## Notas
- Si no se configura SMTP, los correos de activación y recuperación se mostrarán en la consola durante el desarrollo.
- El sistema usa SQLite por defecto para facilitar la instalación local.
