# Configuracion local con credenciales. Copiar como local_settings.py y completar.
SECRET_KEY = 'tu-secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_api',
        'USER': 'root',
        'PASSWORD': 'tu-contrasena',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
