"""
URL configuration for afpuc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path  # Certifique-se de que essa linha está presente.
from afpuc import views  # Importando as views corretamente.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cozinha/', views.cozinha),
    path('criar-conta/', views.criar_conta, name='criar_conta'),
    path('itens/', views.listar_itens, name='listar_itens'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
],
]
