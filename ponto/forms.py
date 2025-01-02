from django import forms
from django.contrib.auth.models import User
from .models import Funcionario, Empresa
from django.contrib.auth.forms import AuthenticationForm
from ponto.utils.telefone import validar_telefone
from ponto.utils.email import validar_email

class RegistroForm(forms.ModelForm):
    """
    Formulário de registro para criação de novos funcionários e usuários Django.

    Atributos:
    username : forms.CharField
        Campo para inserir o nome de usuário.
    password : forms.CharField
        Campo para inserir a senha.
    email : forms.EmailField
        Campo para inserir o e-mail.
    empresa : forms.ModelChoiceField
        Campo para selecionar a empresa associada ao novo funcionário.

    Métodos:
    save(commit=True)
        Salva o novo usuário e o novo funcionário associado ao usuário.
        Retorna o novo funcionário.
    """
    username = forms.CharField(max_length=150, label="Nome de Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    email = forms.EmailField(label="E-mail")
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), label="Empresa")  # Corrigido para Empresa#-

    class Meta:#-
        model = Funcionario#-
        fields = ['empresa']#-
    def save(self, commit=True):
        # Cria o usuário Django
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email']
        )
        # Cria o funcionário vinculado ao usuário
        funcionario = super().save(commit=False)
        funcionario.user = user
        if commit:
            funcionario.save()
        return funcionario

class LoginForm(AuthenticationForm):
    """
    Um formulário de login personalizado que estende o AuthenticationForm do Django.

    Este formulário fornece campos para autenticação de nome de usuário e senha.

    Atributos:
        username (forms.CharField): Um campo para o usuário inserir seu nome de usuário.
            max_length (int): O comprimento máximo do nome de usuário é definido para 150 caracteres.
            label (str): O rótulo para este campo é definido como "Nome de Usuário".

    Nota:
        O campo de senha é herdado da classe AuthenticationForm pai.
    """
    username = forms.CharField(max_length=150, label="Nome de Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

class FuncionarioForm(forms.ModelForm):
    """
    Formulário para criação e validação de funcionários.
    Atributos:
        username (forms.CharField): Campo para o nome de usuário com limite de 150 caracteres.
        email (forms.EmailField): Campo para o e-mail do usuário.
        password (forms.CharField): Campo para a senha do usuário com widget de entrada de senha.
    Meta:
        model (Funcionario): Modelo associado ao formulário.
        fields (list): Lista de campos do modelo a serem incluídos no formulário.
    Métodos:
        clean_telefone(): Valida o campo telefone utilizando a função `validar_telefone`.
        clean_email(): Valida o campo email utilizando a função `validar_email`.
        save(commit=True): Cria um usuário e associa a um funcionário, salvando ambos no banco de dados.
    """
    username = forms.CharField(label="Nome de Usuário", max_length=150)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = Funcionario
        fields = ['empresa', 'telefone']

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        validar_telefone(telefone)
        return telefone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validar_email(email)
        return email
    
    def save(self, commit=True):
        # Cria o usuário primeiro
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        # Cria o funcionário associado ao usuário
        funcionario = super().save(commit=False)
        funcionario.user = user
        if commit:
            funcionario.save()
        return funcionario

class FuncionarioUpdateForm(forms.ModelForm):
    """
    Formulário para atualização de informações do modelo Funcionario, incluindo campos do modelo User associado.
    Campos:
        username (forms.CharField): Campo para o nome de usuário do modelo User.
        email (forms.EmailField): Campo para o e-mail do modelo User.
    Meta:
        model (Funcionario): Modelo Funcionario associado ao formulário.
        fields (list): Lista de campos do modelo Funcionario a serem incluídos no formulário.
    Métodos:
        __init__(self, *args, **kwargs): Inicializa o formulário, preenchendo os campos do User se o funcionário estiver associado a um usuário.
        clean_telefone(self): Valida o campo telefone utilizando a função validar_telefone.
        clean_email(self): Valida o campo email utilizando a função validar_email.
        save(self, commit=True): Salva as alterações nos modelos User e Funcionario.
    """
    username = forms.CharField(label="Nome de Usuário", max_length=150)
    email = forms.EmailField(label="E-mail", max_length=254)

    class Meta:
        model = Funcionario
        fields = ['empresa', 'telefone']
    def __init__(self, *args, **kwargs):
        # Obtenha o usuário relacionado ao funcionário
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Preencha os campos do User no formulário
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        validar_telefone(telefone)
        return telefone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validar_email(email)
        return email

    def save(self, commit=True):
        # Atualiza o modelo User
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        # Atualiza o modelo Funcionario
        funcionario = super().save(commit=False)
        if commit:
            funcionario.save()
        return funcionario

class EmpresaForm(forms.ModelForm):
    """
    Formulário para o modelo Empresa.

    Este formulário é utilizado para criar e atualizar instâncias do modelo Empresa.
    Ele inclui os campos 'nome', 'endereco' e 'telefone'.

    Métodos:
        clean_telefone(): Valida o campo 'telefone' utilizando a função genérica 'validar_telefone'.

    Atributos:
        Meta:
            model (Empresa): O modelo associado a este formulário.
            fields (list): Lista de campos incluídos no formulário.
    """
    class Meta:
        model = Empresa
        fields = ['nome', 'endereco', 'telefone']

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        validar_telefone(telefone)  # Reutiliza a função genérica
        return telefone
