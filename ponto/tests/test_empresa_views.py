from django.test import TestCase
from django.urls import reverse
from ponto.models import Empresa
from django.contrib.auth.models import User


class EmpresaTestCase(TestCase):
    def setUp(self):
        """
        Configuração inicial para os testes:
        - Cria um usuário para autenticação.
        - Cria instâncias de Empresa para os testes.
        """
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.empresa1 = Empresa.objects.create(
            nome="Empresa Teste 1",
            endereco="Rua Teste, 123",
            telefone="(88) 12345-6789"
        )
        self.empresa2 = Empresa.objects.create(
            nome="Empresa Teste 2",
            endereco="Av Teste, 456",
            telefone="(88) 98765-4321"
        )

    def test_listar_empresas(self):
        """
        Testa se a página de listagem de empresas retorna status 200 e exibe as empresas corretamente.
        """
        self.client.login(username='testuser', password='12345')  # Faz login no sistema
        response = self.client.get(reverse('empresa-list'))
        self.assertEqual(response.status_code, 200)  # Verifica se a página carrega corretamente
        self.assertContains(response, "Empresa Teste 1")  # Verifica se a empresa1 está listada
        self.assertContains(response, "Empresa Teste 2")  # Verifica se a empresa2 está listada

    def test_criar_empresa(self):
        """
        Testa se uma nova empresa pode ser criada com sucesso.
        """
        self.client.login(username='testuser', password='12345')  # Faz login no sistema
        response = self.client.post(reverse('empresa-create'), {
            'nome': "Empresa Teste 3",
            'endereco': "Rua Nova, 789",
            'telefone': "(11) 22334-4455"
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após a criação bem-sucedida
        self.assertTrue(Empresa.objects.filter(nome="Empresa Teste 3").exists())  # Verifica se a empresa foi criada

    def test_atualizar_empresa(self):
        """
        Testa se uma empresa existente pode ser atualizada com sucesso.
        """
        self.client.login(username='testuser', password='12345')  # Faz login no sistema
        response = self.client.post(reverse('empresa-update', args=[self.empresa1.id]), {
            'nome': "Empresa Atualizada",
            'endereco': "Rua Alterada, 321",
            'telefone': "(55) 66777-8899"
        })
        self.assertEqual(response.status_code, 302)  # Redireciona após a atualização bem-sucedida
        self.empresa1.refresh_from_db()  # Atualiza o objeto da base de dados
        self.assertEqual(self.empresa1.nome, "Empresa Atualizada")  # Verifica se o nome foi atualizado
        self.assertEqual(self.empresa1.endereco, "Rua Alterada, 321")  # Verifica se o endereço foi atualizado
        self.assertEqual(self.empresa1.telefone, "(55) 66777-8899")  # Verifica se o telefone foi atualizado

    def test_permissao_acesso_nao_autenticado(self):
        """
        Testa se um usuário não autenticado é redirecionado ao tentar acessar as páginas protegidas.
        """
        response_list = self.client.get(reverse('empresa-list'))
        response_create = self.client.get(reverse('empresa-create'))
        response_update = self.client.get(reverse('empresa-update', args=[self.empresa1.id]))
        
        # Verifica que usuários não autenticados não podem acessar
        self.assertNotEqual(response_list.status_code, 200)
        self.assertNotEqual(response_create.status_code, 200)
        self.assertNotEqual(response_update.status_code, 200)
        
        # Verifica os redirecionamentos corretos
        self.assertRedirects(response_list, '/auth/login/?next=/empresas/')
        self.assertRedirects(response_create, '/auth/login/?next=/empresas/nova/')  # Corrigido para "nova"
        self.assertRedirects(response_update, f'/auth/login/?next=/empresas/{self.empresa1.id}/editar/')
