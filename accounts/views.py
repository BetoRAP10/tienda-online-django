from django.contrib.auth.hashers import make_password
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from zeep import Client
from zeep.exceptions import Fault

from .models import User
from .serializers import RegisterSerializer, UserSerializer

COUNTRY_INFO_WSDL = (
    "http://webservices.oorsprong.org/websamples.countryinfo/"
    "CountryInfoService.wso?WSDL"
)
_soap_client = None


def get_soap_client():
    # Se crea una sola vez y se reutiliza (descargar el WSDL en cada
    # request seria lento).
    global _soap_client
    if _soap_client is None:
        _soap_client = Client(COUNTRY_INFO_WSDL)
    return _soap_client


class UserApiViewSet(ModelViewSet):
    """CRUD de usuarios (solo administradores)."""

    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        # La contrasena llega en texto plano desde el cliente: se hashea
        # antes de guardarla.
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # Correccion de seguridad (error #2 del manual): el codigo original
        # hacia request.data["password"] = request.user.password cuando no
        # se enviaba contrasena, lo que SOBRESCRIBIA la contrasena del
        # usuario editado con el hash de quien hace la peticion (por
        # ejemplo, el admin). Aqui simplemente no se toca request.data si
        # no viene password: al ser un PATCH, el serializer deja ese campo
        # sin modificar.
        if "password" in request.data:
            request.data["password"] = make_password(request.data["password"])
        return super().partial_update(request, *args, **kwargs)


class UserView(APIView):
    """Datos personales del usuario autenticado (sin exponer la contrasena)."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterView(CreateAPIView):
    """Registro de usuarios nuevos, sin necesidad de estar autenticado."""

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Usuario registrado exitosamente",
                "user": {"username": user.username, "email": user.email},
            },
            status=201,
        )


class CountryInfoView(APIView):
    """
    Consume el Web Service SOAP publico CountryInfoService (oorsprong.org)
    usando la libreria zeep, y devuelve la info del pais en JSON.

    GET /api/soap/countries/<codigo_iso>/   ej: /api/soap/countries/MX/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, iso_code):
        client = get_soap_client()
        try:
            result = client.service.FullCountryInfo(iso_code.upper())
        except Fault as exc:
            return Response({"detail": str(exc)}, status=400)

        languages = []
        if result.Languages and result.Languages.tLanguage:
            languages = [
                {"codigo": lang.sISOCode, "nombre": lang.sName}
                for lang in result.Languages.tLanguage
            ]

        return Response(
            {
                "codigo_iso": result.sISOCode,
                "nombre": result.sName,
                "capital": result.sCapitalCity,
                "codigo_telefono": result.sPhoneCode,
                "continente": result.sContinentCode,
                "moneda": result.sCurrencyISOCode,
                "bandera": result.sCountryFlag,
                "idiomas": languages,
                "fuente": "SOAP - CountryInfoService (oorsprong.org) via zeep",
            }
        )
