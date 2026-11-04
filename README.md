# tienda_online

API REST de productos y categorías construida con Django + Django REST Framework,
con autenticación JWT, un Web Service SOAP propio consumido con `zeep`, y un
frontend en React (Vite) con login, registro y un Dashboard protegido.

## Backend (Django)

### Estructura

- `products/` — modelos `Category` y `Product` (relación `ForeignKey`), serializers,
  vistas (`ModelViewSet`) y filtro por categoría (`django-filter`).
- `accounts/` — autenticación: `/auth/me/` (datos del usuario logueado),
  `/auth/register/` (registro de usuarios nuevos), y `/soap/countries/<codigo>/`
  (consumo del Web Service SOAP público **CountryInfoService** vía `zeep`).
- `tienda_online/` — configuración del proyecto (settings, urls, JWT, CORS).

### Configuración local

1. Crear y activar el entorno virtual, luego `pip install -r requirements.txt`.
2. Copiar `tienda_online/local_settings.example.py` a `tienda_online/local_settings.py`
   y completar `SECRET_KEY` y las credenciales de MySQL.
3. `python manage.py migrate`
4. `python manage.py createsuperuser` (opcional, para `/admin/`)
5. `python manage.py runserver`

### Endpoints principales

- `POST /api/token/` y `POST /api/token/refresh/` — login JWT (usuario y contraseña).
- `POST /api/auth/register/` — registro de usuario nuevo (sin autenticación).
- `GET /api/auth/me/` — datos del usuario autenticado.
- `GET/POST /api/products/` y `GET/POST /api/categories/` — CRUD de productos y
  categorías (requieren JWT). `/api/products/?category=<id>` filtra por categoría.
- `GET /api/soap/countries/<codigo_iso>/` — información de un país (capital, moneda,
  idiomas, código telefónico) obtenida en tiempo real desde el Web Service SOAP
  público de oorsprong.org a través de `zeep` (requiere JWT).

## Frontend (React + Vite)

Carpeta `frontend/`. Estructura inspirada en el manual de Desarrollo Full Stack
con Django y React: `api/` (llamadas al backend), `context/` y `hooks/`
(`AuthContext`/`useAuth`), `layouts/`, `pages/` (`common`, `client`, `admin`) y
`routes/` (React Router v6).

### Configuración local

1. `cd frontend && npm install`
2. Copiar `.env` con `VITE_BASE_API_URL=http://127.0.0.1:8000` (el backend debe
   estar corriendo en ese puerto, con CORS habilitado para `localhost:5173`).
3. `npm run dev`

### Páginas

- `/` — página de inicio.
- `/login` — inicio de sesión (JWT). El token se guarda en `localStorage` y se
  imprime en la consola del navegador al obtenerse.
- `/register` — registro de usuario nuevo.
- `/dashboard` — panel protegido (requiere sesión iniciada). Muestra los datos
  del usuario autenticado, una frase motivadora obtenida de la API pública
  **Advice Slip** (sin API key), y un formulario para consultar el Web Service
  SOAP de países a través del backend.

## Documentación de las prácticas

Los informes en PDF de cada entrega (Práctica 2, Práctica 3 y RA2) están en la
raíz del repositorio.
