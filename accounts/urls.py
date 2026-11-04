from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CountryInfoView, RegisterView, UserApiViewSet, UserView

router = DefaultRouter()
router.register('users', UserApiViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', UserView.as_view(), name='auth-me'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('soap/countries/<str:iso_code>/', CountryInfoView.as_view(), name='soap-country-info'),
]
