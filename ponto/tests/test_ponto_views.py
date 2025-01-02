from django.test import TestCase
from django.urls import reverse
from ponto.models import Empresa, Funcionario, Ponto
from django.contrib.auth.models import User
from datetime import date, time


class PontoTestCase(TestCase):
    def setUp(self):
        """
        Configuração inicial para os testes:
        - Cria uma empresa.
        - Cria um usuário e um funcionário.
        - Cria registros de ponto.
        """
        self.empresa = Empresa.objects.create(
            nome="Empresa Teste",
            endereco="Rua Teste, 123",
            telefone="(12) 3456-7890"
        )
        self.user = User.objects.create_user(username='user_test', password='12345')
        self.funcionario = Funcionario.objects.create(
            user=self.user,
            empresa=self.empresa,
            telefone="(11) 9988-7766"
        )

        # Criando registros de ponto
        self.ponto1 = Ponto.objects.create(
            funcionario=self.funcionario,
            data=date(2024, 12, 29),
            entrada=time(8, 0),
            intervalo=time(12, 0),
            saida=time(17, 0)
        )
        self.ponto2 = Ponto.objects.create(
            funcionario=self.funcionario,
            data=date(2024, 12, 30),
            entrada=time(9, 0),
            intervalo=time(13, 0),
            saida=time(18, 0)
        )

    def test_listar_pontos(self):
        """
        Testa se a listagem de pontos funciona corretamente para um funcionário autenticado.
        """
        self.client.login(username='user_test', password='12345')  # Faz login
        response = self.client.get(reverse('ponto-list'))
        self.assertEqual(response.status_code, 200)  # A página deve carregar
        self.assertContains(response, "Dec. 29, 2024")
        self.assertContains(response, "Dec. 30, 2024")

    def test_filtro_pontos_por_funcionario(self):
        """
        Testa se o filtro por funcionário funciona corretamente.
        """
        self.client.login(username='user_test', password='12345')  # Faz login
        response = self.client.get(reverse('ponto-list'), {'funcionario': self.funcionario.id})
        print(response.status_code)
        print(response.context['object_list'].values())
        self.assertEqual(response.status_code, 200)  # A página deve carregar
        self.assertContains(response, "Dec. 29, 2024")

    def test_criar_ponto(self):
        """
        Testa se um novo registro de ponto pode ser criado.
        """
        self.client.login(username='user_test', password='12345')  # Faz login
        response = self.client.post(reverse('ponto-create'), {
            'funcionario': self.funcionario.id,
            'data': '2024-12-31',
            'entrada': '08:00',
            'intervalo': '01:00',
            'saida': '17:00'
        })
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento
        self.assertTrue(Ponto.objects.filter(data='2024-12-31').exists())  # Verifica se o ponto foi criado

    def test_atualizar_ponto(self):
        """
        Testa se um registro de ponto existente pode ser atualizado.
        """
        self.client.login(username='user_test', password='12345')  # Faz login
        response = self.client.post(reverse('ponto-update', args=[self.ponto1.id]), {
            'funcionario': self.funcionario.id,
            'data': '2024-12-29',
            'entrada': '08:30',  # Atualiza o horário de entrada
            'intervalo': '12:00',
            'saida': '17:00'
        })
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento
        self.ponto1.refresh_from_db()  # Atualiza o objeto da base de dados
        self.assertEqual(self.ponto1.entrada, time(8, 30))  # Verifica se o horário foi atualizado

    def test_permissao_acesso_nao_autenticado(self):
        """
        Testa se um usuário não autenticado é redirecionado ao tentar acessar as páginas protegidas.
        """
        response_list = self.client.get(reverse('ponto-list'))
        response_create = self.client.get(reverse('ponto-create'))
        response_update = self.client.get(reverse('ponto-update', args=[self.ponto1.id]))
        self.assertNotEqual(response_list.status_code, 200)  # Usuário não autenticado não deve acessar
        self.assertNotEqual(response_create.status_code, 200)  # Usuário não autenticado não deve acessar
        self.assertNotEqual(response_update.status_code, 200)  # Usuário não autenticado não deve acessar
        self.assertRedirects(response_list, '/auth/login/?next=/pontos/')
        self.assertRedirects(response_create, '/auth/login/?next=/pontos/novo/')
        self.assertRedirects(response_update, f'/auth/login/?next=/pontos/{self.ponto1.id}/editar/')
