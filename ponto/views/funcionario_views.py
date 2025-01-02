from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from ponto.models import Funcionario
from ponto.forms import FuncionarioForm, FuncionarioUpdateForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class FuncionarioListView(ListView):
    """
    Uma view baseada em classe que exibe uma lista de objetos Funcionario.

    Atributos:
        model (Model): O modelo que será utilizado para exibir a lista de objetos.
        template_name (str): O nome do template que será renderizado para exibir a lista.

    Métodos Herdados:
        - get_queryset(): Retorna o queryset que será utilizado para exibir a lista de objetos.
        - get_context_data(**kwargs): Retorna o contexto adicional para renderizar o template.
    """
    model = Funcionario
    template_name = 'funcionario_list.html'

@method_decorator(login_required, name='dispatch')
class FuncionarioCreateView(CreateView):
    """
    View para criar um novo Funcionario.

    Atributos:
        model (Model): O modelo que será utilizado para criar o objeto.
        form_class (Form): O formulário que será utilizado para criar o objeto.
        template_name (str): O nome do template que será renderizado.
        success_url (str): A URL para redirecionar após a criação bem-sucedida do objeto.

    Métodos:
        form_valid(form): Exibe uma mensagem de sucesso e chama o método form_valid da superclasse.
    """
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionario-list')

    def form_valid(self, form):
        messages.success(self.request, "Funcionário criado com sucesso!")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class FuncionarioUpdateView(UpdateView):
    """
    View para atualização de um funcionário.

    Esta view utiliza a classe `UpdateView` para fornecer a funcionalidade de atualização de um objeto `Funcionario`.
    Ela utiliza um formulário personalizado `FuncionarioUpdateForm` e renderiza o template `funcionario_form.html`.
    Após a atualização bem-sucedida, redireciona o usuário para a lista de funcionários.

    Atributos:
        model (Model): O modelo que será atualizado, neste caso, `Funcionario`.
        form_class (Form): O formulário utilizado para atualizar o modelo, neste caso, `FuncionarioUpdateForm`.
        template_name (str): O nome do template que será renderizado, neste caso, `funcionario_form.html`.
        success_url (str): A URL para redirecionamento após a atualização bem-sucedida, neste caso, a URL nomeada 'funcionario-list'.

    Métodos:
        get_form_kwargs(self):
            Sobrescreve o método `get_form_kwargs` para adicionar o usuário atual aos argumentos do formulário.

        form_valid(self, form):
            Sobrescreve o método `form_valid` para adicionar uma mensagem de sucesso após a atualização bem-sucedida.
    """
    model = Funcionario
    form_class = FuncionarioUpdateForm
    template_name = 'funcionario_form.html'
    success_url = reverse_lazy('funcionario-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Funcionário atualizado com sucesso!")
        return super().form_valid(form)