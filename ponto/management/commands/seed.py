from django.core.management.base import BaseCommand
from ponto.models import Empresa

class Command(BaseCommand):
    help = 'Cria dados iniciais no banco de dados'

    def handle(self, *args, **kwargs):
        # Criar uma empresa
        empresa, created = Empresa.objects.get_or_create(
            nome="Empresa M2",
            endereco="Rua Exemplo, 123",
            telefone="(11) 1234-5678"
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Empresa criada com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('A empresa já existe no banco de dados.'))
