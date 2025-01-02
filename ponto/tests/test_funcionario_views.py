from django.test import TestCase
from django.urls import reverse
from ponto.models import Funcionario, Empresa
from django.contrib.auth.models import User


class FuncionarioTestCase(TestCase):
    def setUp(self):
        """
        Configuração inicial para os testes:
        - Cria um usuário para autenticação.
        - Cria uma empresa.
        - Cria um funcionário para o usuário.
        """
        self.user = User.objects.create_user(username='user_test', email='user_test@example.com', password='12345')
        self.empresa = Empresa.objects.create(
            nome="Empresa Teste",
            endereco="Rua Teste, 123",
            telefone="(12) 3456-4789"
        )
        self.funcionario1 = Funcionario.objects.create(
            user=self.user,
            empresa=self.empresa,
            telefone="(98) 7654-4321"
        )

    def test_listar_funcionarios(self):
        """
        Testa se a página de listagem de funcionários retorna status 200 e exibe os funcionários corretamente.
        """
        self.client.login(username='user_test', password='12345')  # Faz login no sistema
        response = self.client.get(reverse('funcionario-list'))
        self.assertEqual(response.status_code, 200)  # Verifica se a página carrega corretamente
        self.assertContains(response, "user_test")  # Verifica se o funcionário com usuário está listado

    def test_atualizar_funcionario(self):
        """
        Testa se um funcionário existente pode ser atualizado com sucesso.
        """
        self.client.login(username='user_test', password='12345')  # Faz login no sistema
        response = self.client.post(reverse('funcionario-update', args=[self.funcionario1.id]), {
            'username': 'user_test',  # Nome de usuário existente
            'email': 'user_test@example.com',  # Email existente
            'empresa': self.empresa.id,  # Empresa associada
            'telefone': "(55) 6677-8899"  # Novo telefone
        })
        self.assertEqual(response.status_code, 302)  # Verifica o redirecionamento
        self.funcionario1.refresh_from_db()  # Atualiza o objeto da base de dados
        self.assertEqual(self.funcionario1.telefone, "(55) 6677-8899")  # Verifica se o telefone foi atualizado

    def test_permissao_acesso_nao_autenticado(self):
        """
        Testa se um usuário não autenticado é redirecionado ao tentar acessar as páginas protegidas.
        """
        response_list = self.client.get(reverse('funcionario-list'))
        response_create = self.client.get(reverse('funcionario-create'))
        response_update = self.client.get(reverse('funcionario-update', args=[self.funcionario1.id]))
        self.assertNotEqual(response_list.status_code, 200)  # Usuário não autenticado não deve acessar
        self.assertNotEqual(response_create.status_code, 200)  # Usuário não autenticado não deve acessar
        self.assertNotEqual(response_update.status_code, 200)  # Usuário não autenticado não deve acessar
        self.assertRedirects(response_list, '/auth/login/?next=/funcionarios/')
        self.assertRedirects(response_create, '/auth/login/?next=/funcionarios/novo/')
        self.assertRedirects(response_update, f'/auth/login/?next=/funcionarios/{self.funcionario1.id}/editar/')
