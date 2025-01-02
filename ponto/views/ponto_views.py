from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from ponto.models import Ponto, Funcionario
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class PontoListView(ListView):
    """
    Exibe uma lista de objetos Ponto com base nos filtros fornecidos.

    Atributos:
        model (Model): O modelo que será utilizado para listar os objetos.
        template_name (str): O nome do template que será renderizado.

    Métodos:
        get_queryset(): Retorna o queryset filtrado com base nos parâmetros de consulta fornecidos.
        get_context_data(**kwargs): Adiciona dados adicionais ao contexto do template.

    Filtros de consulta:
        funcionario (int): ID do funcionário para filtrar os pontos.
        data_inicio (str): Data de início para filtrar os pontos (formato YYYY-MM-DD).
        data_fim (str): Data de fim para filtrar os pontos (formato YYYY-MM-DD).

    Contexto adicional:
        funcionarios (QuerySet): Lista de todos os funcionários.
        data_inicio (str): Valor do parâmetro de consulta 'data_inicio'.
        data_fim (str): Valor do parâmetro de consulta 'data_fim'.
    """
    model = Ponto
    template_name = 'ponto_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        funcionario_id = self.request.GET.get('funcionario')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if funcionario_id:
            queryset = queryset.filter(funcionario_id=funcionario_id)
        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funcionarios'] = Funcionario.objects.all()
        context['data_inicio'] = self.request.GET.get('data_inicio', '')
        context['data_fim'] = self.request.GET.get('data_fim', '')
        return context

@method_decorator(login_required, name='dispatch')
class PontoCreateView(CreateView):
    """
    View para criar um novo registro de ponto.

    Atributos:
        model (Model): O modelo utilizado para criar o registro de ponto.
        fields (list): Lista de campos do modelo que serão exibidos no formulário.
        template_name (str): Nome do template utilizado para renderizar o formulário.
        success_url (str): URL para redirecionamento após a criação bem-sucedida do registro de ponto.

    Métodos:
        form_valid(form):
            Exibe uma mensagem de sucesso e chama o método form_valid da superclasse.
            Args:
                form (Form): O formulário que foi validado.
            Returns:
                HttpResponse: Resposta HTTP após o formulário ser validado.
    """
    model = Ponto
    fields = ['funcionario', 'data', 'entrada', 'intervalo', 'saida']
    template_name = 'ponto_form.html'
    success_url = reverse_lazy('ponto-list')

    def form_valid(self, form):
        messages.success(self.request, "Registro de ponto criado com sucesso!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class PontoUpdateView(UpdateView):
    """
    View para atualização de registros de ponto.

    Atributos:
        model (Model): O modelo que será atualizado.
        fields (list): Lista de campos que serão exibidos no formulário.
        template_name (str): Nome do template que será renderizado.
        success_url (str): URL para redirecionamento após a atualização bem-sucedida.

    Métodos:
        form_valid(form):
            Exibe uma mensagem de sucesso e chama o método form_valid da classe pai.
    """
    model = Ponto
    fields = ['funcionario', 'data', 'entrada', 'intervalo', 'saida']
    template_name = 'ponto_form.html'
    success_url = reverse_lazy('ponto-list')

    def form_valid(self, form):
        messages.success(self.request, "Registro de ponto atualizado com sucesso!")
        return super().form_valid(form)
