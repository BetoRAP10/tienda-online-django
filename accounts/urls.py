from django.urls import path
from .views import MeView, RegisterView, CountryInfoView

urlpatterns = [
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("soap/countries/<str:iso_code>/", CountryInfoView.as_view(), name="soap-country-info"),
]
