"""
URL configuration for XYUnionAuth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

from XYUnionAuth.views import user, permissions

schema_view = get_schema_view(
    openapi.Info(
        title="XYUnionAuth API",
        default_version='v1',
        description="Welcome to the XYUnionAuth",
        license=openapi.License(name="MIT"),
    ),
    public=True
)

urlpatterns = [
    re_path(r'^doc(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    
    # User
    path('user/login/', user.login),
    path('user/register/', user.register),
    path('user/verify_token/', user.verify_token),
    
    # Permissions
    path('permissions/policies/', permissions.policies),
    path('permissions/check_permission/', permissions.check_permission)
]
