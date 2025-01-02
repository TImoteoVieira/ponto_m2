from rest_framework import serializers
from .models import Empresa, Funcionario, Ponto

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

class PontoSerializer(serializers.ModelSerializer):
    horas_trabalhadas = serializers.ReadOnlyField()

    class Meta:
        model = Ponto
        fields = '__all__'