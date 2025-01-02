from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('ponto.urls.auth')),
    path('', lambda request: render(request, 'home.html'), name='home'),
    path('empresas/', include('ponto.urls.empresas')),  # Criamos um novo arquivo de URLs por entidade
    path('funcionarios/', include('ponto.urls.funcionarios')),
    path('pontos/', include('ponto.urls.pontos')),
]
