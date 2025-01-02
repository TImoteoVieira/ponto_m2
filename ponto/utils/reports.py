import fitz
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.shortcuts import render, redirect, get_object_or_404
from ponto.models import Ponto, Funcionario

def gerar_relatorio(request):
    """
    Gera um relatório em formato PDF com os registros de ponto dos funcionários, 
    filtrando por funcionário e intervalo de datas, se fornecidos.

    Parâmetros:
    request (HttpRequest): Objeto de requisição HTTP contendo os parâmetros de filtro.

    Parâmetros de filtro:
    - funcionario: ID do funcionário para filtrar os registros de ponto.
    - data_inicio: Data de início para filtrar os registros de ponto.
    - data_fim: Data de fim para filtrar os registros de ponto.

    O relatório inclui:
    - Data
    - Horário de entrada
    - Intervalo
    - Horário de saída
    - Horas trabalhadas
    - Atrasos
    - Horas extras

    O PDF gerado contém um cabeçalho com informações do funcionário (se fornecido), 
    data de emissão e observações sobre a jornada de trabalho. 
    Os registros de ponto são listados em uma tabela, e os totais de atrasos e horas extras 
    são calculados e exibidos ao final do relatório.

    Retorna:
    HttpResponse: Resposta HTTP contendo o PDF gerado como anexo.
    """
    # Captura os parâmetros de filtro
    funcionario_id = request.GET.get('funcionario')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Filtra os pontos com base nos parâmetros
    pontos = Ponto.objects.all().order_by('data')
    funcionario = None
    if funcionario_id:
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        pontos = pontos.filter(funcionario=funcionario)
    if data_inicio:
        pontos = pontos.filter(data__gte=data_inicio)
    if data_fim:
        pontos = pontos.filter(data__lte=data_fim)

    # Funções auxiliares para cálculos
    def calcular_atrasos_e_extras(ponto):
        """
        Calcula atrasos e horas extras em formato hh:mm:ss.
        Retorna dois valores: atraso, extra.
        """
        horas_regulamentares = 8  # Horas por dia
        atraso = timedelta(0)
        extra = timedelta(0)

        try:
            if ponto.entrada and ponto.saida:
                # Calcula tempo trabalhado real (removendo intervalo)
                entrada = datetime.combine(ponto.data, ponto.entrada)
                saida = datetime.combine(ponto.data, ponto.saida)
                intervalo = timedelta(
                    hours=ponto.intervalo.hour, minutes=ponto.intervalo.minute
                ) if ponto.intervalo else timedelta(0)
                tempo_trabalhado = saida - entrada - intervalo

                # Verifica atraso se as horas trabalhadas forem menores que 8h
                if tempo_trabalhado < timedelta(hours=8):
                    atraso = timedelta(hours=8) - tempo_trabalhado

                # Calcula horas extras se exceder 8h
                if tempo_trabalhado > timedelta(hours=8):
                    extra = tempo_trabalhado - timedelta(hours=8)

        except Exception as e:
            # Log do erro para depuração (se necessário)
            print(f"Erro ao calcular atrasos e extras para o ponto {ponto.id}: {e}")
        
        return atraso, extra

    # Totais acumulados
    total_atrasos = timedelta(0)
    total_extras = timedelta(0)

    # Crie o documento PDF
    pdf = fitz.open()
    page = pdf.new_page()

    # Adicione cabeçalho com informações
    titulo = "Relatório de Pontos de Funcionários"
    if funcionario:
        titulo += f" - {funcionario.user.username}"
    page.insert_text(
        (50, 50), 
        titulo, 
        fontsize=18, fontname="courier-bold", color=(0, 0, 0)
    )
    if funcionario:
        page.insert_text(
            (50, 80), 
            f"Funcionário: {funcionario.user.username} | Empresa: {funcionario.empresa.nome}", 
            fontsize=12, fontname="courier", color=(0, 0, 0)
        )
    page.insert_text(
        (50, 100), 
        f"Emitido em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 
        fontsize=10, fontname="courier", color=(0, 0, 0)
    )
    page.insert_text(
        (50, 120), 
        f"Observação: Jornada semanal de 40h (8h às 17h, com 1h de intervalo)", 
        fontsize=10, fontname="courier", color=(0, 0, 0)
    )

    # Adicione cabeçalho da tabela
    y = 150
    headers = [
        "Data", "Entrada", "Intervalo", "Saída", "Horas Trabalhadas", "Atrasos", "Horas Extras"
    ]
    col_widths = [70, 60, 70, 60, 120, 80, 80]  # Largura das colunas

    # Desenhe o cabeçalho
    x = 50
    for i, header in enumerate(headers):
        page.insert_text((x, y), header, fontsize=10, fontname="courier-bold", color=(0, 0, 0))
        x += col_widths[i]
    y += 20

    # Adicione os registros de ponto
    for ponto in pontos:
        data = ponto.data.strftime('%d/%m/%Y')
        entrada = ponto.entrada.strftime('%H:%M') if ponto.entrada else "-"
        intervalo = ponto.intervalo.strftime('%H:%M') if ponto.intervalo else "-"
        saida = ponto.saida.strftime('%H:%M') if ponto.saida else "-"
        horas_trabalhadas = ponto.horas_trabalhadas() if ponto.horas_trabalhadas() != "N/A" else "-"

        atraso, extra = calcular_atrasos_e_extras(ponto)
        total_atrasos += atraso
        total_extras += extra

        # Organize os dados em colunas
        valores = [
            data, entrada, intervalo, saida, horas_trabalhadas,
            str(atraso) if atraso > timedelta(0) else "-",
            str(extra) if extra > timedelta(0) else "-"
        ]
        x = 50
        for i, valor in enumerate(valores):
            page.insert_text((x, y), valor, fontsize=10, fontname="courier", color=(0, 0, 0))
            x += col_widths[i]
        y += 15

        # Quebra de página se o espaço vertical acabar
        if y > 770:
            page = pdf.new_page()
            y = 50

    # Adicione os totais ao final da tabela
    y += 20
    page.insert_text((50, y), f"Totais:", fontsize=12, fontname="courier-bold", color=(0, 0, 0))
    y += 15
    page.insert_text((50, y), f"Total de Atrasos: {str(total_atrasos)}", fontsize=10, fontname="courier", color=(0, 0, 0))
    y += 15
    page.insert_text((50, y), f"Total de Horas Extras: {str(total_extras)}", fontsize=10, fontname="courier", color=(0, 0, 0))

    # Salve o PDF em um buffer e retorne como resposta HTTP
    pdf_buffer = pdf.write()
    pdf.close()

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_pontos.pdf"'
    return response