from django.urls import path
from ponto.views.auth_views import registrar_usuario, login_usuario, logout_usuario
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('registrar/', registrar_usuario, name='registrar'),
    path('login/', login_usuario, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
