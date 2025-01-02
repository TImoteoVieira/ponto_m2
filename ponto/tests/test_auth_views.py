from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ponto.models import Empresa, Funcionario

class AuthTestCase(TestCase):
    def setUp(self):
        """
        Configuração inicial para os testes:
        - Cria uma empresa para associar usuários.
        - Cria um usuário de teste.
        """
        self.empresa = Empresa.objects.create(
            nome="Empresa Teste",
            endereco="Rua Exemplo, 123",
            telefone="(11) 1234-5678"
        )
        self.user = User.objects.create_user(username="user_test", password="12345")
        Funcionario.objects.create(
            user=self.user,
            empresa=self.empresa
        )
    
    def test_registrar_usuario_sucesso(self):
        """
        Testa se um novo usuário pode ser registrado com sucesso.
        """
        response = self.client.post(reverse('registrar'), {
            'username': 'novo_user',
            'password': 'senha_segura',
            'email': 'novo@user.com',
            'empresa': self.empresa.id
        })
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento
        self.assertTrue(User.objects.filter(username='novo_user').exists())  # Confirma criação do usuário
    
    def test_registrar_usuario_falha(self):
        """
        Testa falha no registro com dados inválidos.
        """
        response = self.client.post(reverse('registrar'), {
            'username': '',  # Nome de usuário inválido
            'password': 'senha_segura',
            'email': 'email_invalido',
            'empresa': self.empresa.id
        })
        self.assertEqual(response.status_code, 200)  # Fica na mesma página
        self.assertContains(response, "This field is required.")
    
    def test_login_usuario_sucesso(self):
        """
        Testa se o login funciona com credenciais corretas.
        """
        response = self.client.post(reverse('login'), {
            'username': 'user_test',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionamento após login
        self.assertTrue('_auth_user_id' in self.client.session)  # Verifica se o usuário está logado
    
    def test_login_usuario_falha(self):
        """
        Testa se o login falha com credenciais incorretas.
        """
        response = self.client.post(reverse('login'), {
            'username': 'user_test',
            'password': 'senha_errada'
        })
        self.assertEqual(response.status_code, 200)  # Página de login recarregada
        self.assertContains(response, "Please enter a correct username and password.")
    
    def test_logout_usuario(self):
        """
        Testa se o logout funciona corretamente.
        """
        self.client.login(username='user_test', password='12345')  # Realiza login
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)  # Verifica se o usuário está deslogado
