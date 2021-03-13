"""chatire URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include

from rest_framework_jwt.views import refresh_jwt_token

from chat.views import raise_404

urlpatterns = [
    path('admin/', admin.site.urls),

    # Custom URL's
    path('auth/', include('djoser.urls')),

    # disable the old endpoint (Order is important)
    path('auth/jwt/refresh/', raise_404),

    # Register the new URL under an ambigous name
    path('this/is/hard/to/find/', refresh_jwt_token),

    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('chat.urls'))
]
