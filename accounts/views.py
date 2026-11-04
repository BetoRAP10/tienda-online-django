from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from zeep import Client
from zeep.exceptions import Fault

from .serializers import UserSerializer, RegisterSerializer

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


class MeView(APIView):
    """Devuelve los datos del usuario autenticado (requiere JWT)."""

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
            status=status.HTTP_201_CREATED,
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
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

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
