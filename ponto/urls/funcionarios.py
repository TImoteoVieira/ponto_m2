from django.urls import path
from ponto.views.funcionario_views import FuncionarioListView, FuncionarioCreateView, FuncionarioUpdateView
from ponto.utils.reports import gerar_relatorio

urlpatterns = [
    path('', FuncionarioListView.as_view(), name='funcionario-list'),
    path('novo/', FuncionarioCreateView.as_view(), name='funcionario-create'),
    path('<int:pk>/editar/', FuncionarioUpdateView.as_view(), name='funcionario-update'),
    path('<int:funcionario_id>/relatorio/', gerar_relatorio, name='funcionario-relatorio'),
]
