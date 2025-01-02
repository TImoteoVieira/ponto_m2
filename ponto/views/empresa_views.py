from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from ponto.models import Empresa
from ponto.forms import EmpresaForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class EmpresaListView(ListView):
    """
    Uma view baseada em classe que exibe uma lista de objetos do modelo Empresa.

    Atributos:
        model (Model): O modelo que será utilizado para exibir a lista de objetos.
        template_name (str): O nome do template que será renderizado para exibir a lista de objetos.

    Métodos Herdados:
        - get_queryset(): Retorna o queryset que será utilizado para exibir a lista de objetos.
        - get_context_data(**kwargs): Retorna o contexto que será passado para o template.
        - get_template_names(): Retorna a lista de nomes de templates que serão utilizados para renderizar a view.
    """
    model = Empresa
    template_name = 'empresa_list.html'

@method_decorator(login_required, name='dispatch')
class EmpresaCreateView(CreateView):
    """
    View para criação de uma nova instância de Empresa.

    Atributos:
        model (Model): O modelo que será utilizado para criar a nova instância.
        form_class (Form): O formulário que será utilizado para criar a nova instância.
        template_name (str): O nome do template que será renderizado.
        success_url (str): A URL para redirecionamento após a criação bem-sucedida.

    Métodos:
        form_valid(form): Exibe uma mensagem de sucesso e chama o método form_valid da classe pai.
    """
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa_form.html'
    success_url = reverse_lazy('empresa-list')

    def form_valid(self, form):
        messages.success(self.request, "Empresa criada com sucesso!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EmpresaUpdateView(UpdateView):
    """
    View para atualização de uma instância do modelo Empresa.

    Atributos:
        model (Model): O modelo que será atualizado.
        form_class (Form): O formulário utilizado para atualizar a instância do modelo.
        template_name (str): O template utilizado para renderizar a página de atualização.
        success_url (str): A URL para redirecionamento após a atualização bem-sucedida.

    Métodos:
        form_valid(form): Exibe uma mensagem de sucesso e chama o método form_valid da classe pai.
    """
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa_form.html'
    success_url = reverse_lazy('empresa-list')

    def form_valid(self, form):
        messages.success(self.request, "Empresa atualizada com sucesso!")
        return super().form_valid(form)
