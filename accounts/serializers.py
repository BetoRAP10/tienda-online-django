from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el CRUD de usuarios y para el endpoint de datos
    personales (/auth/me/).

    Correccion de seguridad (error #1 del manual): el manual original
    incluye 'password' como un campo mas en la respuesta, exponiendo el
    hash de la contrasena en cualquier GET (incluido /auth/me/). Aqui se
    marca 'password' como write_only, para que se pueda enviar al crear o
    actualizar un usuario, pero nunca se devuelva en una respuesta.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'telefono', 'password', 'is_active', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'telefono']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
