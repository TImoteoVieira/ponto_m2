from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ponto.forms import RegistroForm, LoginForm

def registrar_usuario(request):
    """
    Esta função lida com o registro de usuários. Ela verifica se o método da requisição é POST.
    Se for, processa os dados do formulário, valida-os e salva o usuário se for válido.
    Se o método da requisição não for POST, cria um formulário de registro vazio.
    A função então renderiza o template de registro com o formulário.

    Parâmetros:
    request (HttpRequest): O objeto de requisição contendo os dados de entrada do usuário.

    Retorna:
    HttpResponse: O template de registro renderizado com o formulário.
    """
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário registrado com sucesso!")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registrar.html', {'form': form})

def login_usuario(request):
    """
    Função de visualização para realizar o login de um usuário.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.

    Retorna:
        HttpResponse: Redireciona para a página inicial se o login for bem-sucedido,
                      caso contrário, renderiza a página de login com o formulário.

    Comportamento:
        - Se o método da solicitação for 'POST', tenta autenticar o usuário com os dados fornecidos.
        - Se o formulário de login for válido, autentica o usuário e redireciona para a página inicial.
        - Se o método da solicitação não for 'POST', exibe um formulário de login vazio.
    """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_usuario(request):
    """
    Faz o logout do usuário e redireciona para a página de login.

    Args:
        request (HttpRequest): O objeto de solicitação HTTP.

    Returns:
        HttpResponseRedirect: Redireciona o usuário para a página de login com uma mensagem de sucesso.
    """
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect('login')