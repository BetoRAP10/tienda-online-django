from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Login con email en vez de username (corrección pedida por la práctica,
    # manual paginas 7-8).
    email = models.EmailField(unique=True)

    # Campo extra elegido para esta practica: telefono de contacto del
    # cliente de la tienda.
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Telefono')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
