from django.db import models
from django.utils.timezone import now, localtime
from django.contrib.auth.models import User

class Empresa(models.Model):
    """
    A classe Empresa representa uma entidade empresarial com informações básicas como nome, endereço e telefone.
    Atributos:
        nome (str): O nome da empresa.
        endereco (str): O endereço da empresa.
        telefone (str): O número de telefone da empresa.
    Métodos:
        __str__(): Retorna o nome da empresa como sua representação em string.
    """
    nome = models.CharField(max_length=255)
    endereco = models.TextField()
    telefone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    """
        Uma classe usada para representar um Funcionário.

        Atributos
        ---------
            Um relacionamento um-para-um com o modelo User. Pode ser nulo ou em branco.
            Um relacionamento de chave estrangeira com o modelo Empresa. Não pode ser nulo ou em branco.
            Um campo de caracteres para armazenar o número de telefone do funcionário. Pode ser nulo ou em branco.

        Métodos
            Retorna o nome de usuário do usuário associado, se existir, caso contrário, retorna "Funcionário sem usuário".
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='funcionario', null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='funcionarios')
    telefone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username if self.user else "Funcionário sem usuário"


class Ponto(models.Model):
    """
    A classe Ponto representa o registro de ponto de um funcionário em um determinado dia.

    Atributos:
        funcionario (ForeignKey): Referência ao funcionário que registrou o ponto.
        data (DateField): Data do registro do ponto.
        entrada (TimeField): Horário de entrada do funcionário.
        intervalo (TimeField): Horário de início do intervalo do funcionário.
        saida (TimeField): Horário de saída do funcionário.

    Métodos:
        horas_trabalhadas():
            Calcula e retorna o total de horas trabalhadas no formato "Xh Ym".
            Se os horários de entrada ou saída não estiverem definidos, retorna "N/A".
    """
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='pontos')
    data = models.DateField(default=now)
    entrada = models.TimeField(null=True, blank=True)
    intervalo = models.TimeField(null=True, blank=True)
    saida = models.TimeField(null=True, blank=True)

    def horas_trabalhadas(self):
        if self.entrada and self.saida:
            # Converte entrada e saída para o horário local
            entrada_local = localtime().replace(hour=self.entrada.hour, minute=self.entrada.minute)
            saida_local = localtime().replace(hour=self.saida.hour, minute=self.saida.minute)

            # Cálculo de horas trabalhadas
            entrada_delta = entrada_local.hour * 60 + entrada_local.minute
            saida_delta = saida_local.hour * 60 + saida_local.minute
            intervalo_delta = (
                self.intervalo.hour * 60 + self.intervalo.minute
                if self.intervalo else 0
            )
            total_trabalhado = saida_delta - entrada_delta - intervalo_delta
            return f"{total_trabalhado // 60}h {total_trabalhado % 60}m"
        return "N/A"
