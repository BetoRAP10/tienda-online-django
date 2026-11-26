# Imagen del Backend (Django)
FROM python:3.12-slim

WORKDIR /app

# Herramientas del sistema necesarias para compilar mysqlclient
# (el conector de Python hacia MySQL) dentro del contenedor.
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Aplica las migraciones pendientes y arranca el servidor escuchando en
# todas las interfaces para que sea accesible desde fuera del contenedor.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
