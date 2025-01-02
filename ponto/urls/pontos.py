from django.urls import path
from ponto.views.ponto_views import PontoListView, PontoCreateView, PontoUpdateView
from ponto.utils.reports import gerar_relatorio

urlpatterns = [
    path('', PontoListView.as_view(), name='ponto-list'),
    path('novo/', PontoCreateView.as_view(), name='ponto-create'),
    path('<int:pk>/editar/', PontoUpdateView.as_view(), name='ponto-update'),
    path('relatorio/', gerar_relatorio, name='relatorio'),

]
