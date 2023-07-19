"""django_boilerplate_with_multitenant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

from django_boilerplate_with_multitenant.router import OptionalSlashDefaultRouter
from users.views import CustomTokenObtainPairView, TokenGoogleView, UserProfileVIew

schema_view = get_schema_view(
    openapi.Info(
        title="Django Boilerplate with Multitenant",
        default_version='v1',
        description="django boilerplate with multiple tenants",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="azadhmhd@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = OptionalSlashDefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    re_path('api/token/?', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path('api/refresh/?', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('api/google/?', TokenGoogleView.as_view(), name='google_sign_in'),
    re_path('user-profile/?', UserProfileVIew.as_view()),
    # documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
