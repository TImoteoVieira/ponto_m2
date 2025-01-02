from django.urls import path
from ponto.views.empresa_views import EmpresaListView, EmpresaCreateView, EmpresaUpdateView

urlpatterns = [
    path('', EmpresaListView.as_view(), name='empresa-list'),
    path('nova/', EmpresaCreateView.as_view(), name='empresa-create'),
    path('<int:pk>/editar/', EmpresaUpdateView.as_view(), name='empresa-update'),
]
