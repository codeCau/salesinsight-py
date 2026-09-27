"""
SalesInsight PY — Análise de Dados de Vendas com Python
Módulo 01 - Escopo Semanas 01 a 05
Etapa 5: RF01 ao RF05 (Dataset, Inspeção, Limpeza, Derivações e Métricas Agregadas)
"""

import csv
import random
import re
from datetime import datetime, timedelta


# ==========================================
# RF01 - GERAÇÃO E CARGA DO DATASET
# ==========================================
def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """Gera um dataset sintético de vendas com dados inconsistentes e grava em CSV."""
    random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headset"]
    categorias = {
        "Notebook": "Computadores", "Smartphone": "Celulares",
        "Tablet": "Celulares", "Monitor": "Computadores",
        "Teclado": "Perifericos", "Mouse": "Perifericos",
        "Headset": "Perifericos"
    }
    precos = {
        "Notebook": 3500, "Smartphone": 2200, "Tablet": 1800,
        "Monitor": 1200, "Teclado": 250, "Mouse": 120, "Headset": 350
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    data_inicio = datetime(2025, 1, 1)
    colunas = [
        "id_venda", "data_venda", "cliente", "produto",
        "categoria", "regiao", "quantidade", "preco_unitario"
    ]

    with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()

        for i in range(n_registros):
            produto = random.choice(produtos)
            categoria = categorias[produto]
            quantidade = random.randint(1, 10)
            preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
            data = data_inicio + timedelta(days=random.randint(0, 364))
            data_txt = data.strftime("%Y-%m-%d")
            cliente = f"Cliente_{random.randint(1, 50):03d}"

            if random.random() < 0.05:
                quantidade = ""
            if random.random() < 0.04:
                preco = ""
            if random.random() < 0.06:
                produto = " " + produto + " "
            if random.random() < 0.03:
                data_txt = "DATA INVALIDA"
            if random.random() < 0.10:
                cliente = random.choice([
                    cliente.upper().replace("_", "-"),
                    cliente + "!!",
                    " " + cliente,
                    cliente.replace("Cliente_", "cliente#"),
                ])

            escritor.writerow({
                "id_venda": i + 1,
                "data_venda": data_txt,
                "cliente": cliente,
                "produto": produto,
                "categoria": categoria,
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco,
            })

    print(f"[RF01] Dataset pronto em '{caminho_csv}'.")


def carregar_dataset(caminho_csv="vendas.csv"):
    """Lê o arquivo CSV e retorna uma lista de dicionários."""
    with open(caminho_csv, "r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        return list(leitor)


# ==========================================
# RF02 - INSPEÇÃO DOS DADOS BRUTOS
# ==========================================
def inspecionar_dados(registros):
    """Exibe no console informações estruturais e contagem de campos vazios."""
    total = len(registros)
    colunas = list(registros[0].keys()) if registros else []
    nulos = {col: 0 for col in colunas}

    for linha in registros:
        for col in colunas:
            if linha.get(col, "").strip() == "":
                nulos[col] += 1

    print("\n" + "=" * 50)
    print("=== RF02: INSPEÇÃO INICIAL DO DATASET ===")
    print("=" * 50)
    print(f"Total de registros: {total}")
    print(f"Colunas: {colunas}")
    print(f"Campos nulos identificados: {nulos}")
    return registros


# ==========================================
# RF03 - LIMPEZA E TRATAMENTO DOS DADOS
# ==========================================
def limpar_dados(registros):
    """Limpa textos, converte tipos numéricos/datas e descarta nulos críticos."""
    relatorio = {
        "iniciais": len(registros),
        "removidos_data": 0,
        "removidos_nulos": 0,
        "finais": 0
    }
    padrao_cliente = re.compile(r"^Cliente_\d{3}$", flags=re.IGNORECASE)
    limpos = []

    for linha in registros:
        for campo in ("cliente", "produto", "categoria", "regiao"):
            linha[campo] = linha[campo].strip()

        try:
            linha["data_venda"] = datetime.strptime(linha["data_venda"], "%Y-%m-%d")
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

        if linha["quantidade"] == "" or linha["preco_unitario"] == "":
            relatorio["removidos_nulos"] += 1
            continue

        linha["quantidade"] = int(float(linha["quantidade"]))
        linha["preco_unitario"] = float(linha["preco_unitario"])

        nome_limpo = re.sub(r"[^A-Za-z0-9_]", "", linha["cliente"])
        linha["cliente"] = nome_limpo
        linha["cliente_fora_do_padrao"] = padrao_cliente.match(nome_limpo) is None

        limpos.append(linha)

    relatorio["finais"] = len(limpos)

    print("\n" + "=" * 50)
    print("=== RF03: RELATÓRIO DE LIMPEZA ===")
    print("=" * 50)
    print(f"Registros iniciais:     {relatorio['iniciais']}")
    print(f"Descartados por data:   {relatorio['removidos_data']}")
    print(f"Descartados por nulos:  {relatorio['removidos_nulos']}")
    print(f"Registros higienizados: {relatorio['finais']}")

    return limpos, relatorio


# ==========================================
# RF04 - CRIAÇÃO DE COLUNAS DERIVADAS
# ==========================================
def criar_colunas_derivadas(registros):
    """Calcula receita total, extrai componentes temporais e classifica faixas."""
    meses_nomes = [
        "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    for r in registros:
        r["receita_total"] = round(r["quantidade"] * r["preco_unitario"], 2)

        data: datetime = r["data_venda"]
        r["mes"] = data.month
        r["mes_nome"] = meses_nomes[data.month]
        r["ano"] = data.year

        if data.month <= 3:
            r["trimestre"] = "Q1"
        elif data.month <= 6:
            r["trimestre"] = "Q2"
        elif data.month <= 9:
            r["trimestre"] = "Q3"
        else:
            r["trimestre"] = "Q4"

        preco = r["preco_unitario"]
        if preco < 500:
            r["faixa_receita_item"] = "Baixo Valor"
        elif preco <= 2000:
            r["faixa_receita_item"] = "Médio Valor"
        else:
            r["faixa_receita_item"] = "Alto Valor"

    print("\n" + "=" * 50)
    print("=== RF04: COLUNAS DERIVADAS CRIADAS ===")
    print("=" * 50)
    print("Novas colunas geradas: receita_total, mes, mes_nome, ano, trimestre, faixa_receita_item")

    return registros


# ==========================================
# RF05 - CÁLCULO DE MÉTRICAS ANALÍTICAS
# ==========================================
def calcular_metricas(registros):
    """
    Calcula agregações de faturamento temporal, produtos mais vendidos,
    receita por categoria e eficiência regional em passada única O(n).
    """
    mensal = {}
    produtos_rev = {}
    produtos_qtd = {}
    categorias_rev = {}
    regioes_rev = {}
    regioes_qtd_transacoes = {}

    receita_global = 0.0
    itens_globais = 0

    for r in registros:
        receita = r["receita_total"]
        qtd = r["quantidade"]
        chave_mes = (r["ano"], r["mes"], r["mes_nome"], r["trimestre"])

        receita_global += receita
        itens_globais += qtd

        # Agrupamento temporal
        if chave_mes not in mensal:
            mensal[chave_mes] = {"receita": 0.0, "itens": 0, "transacoes": 0}
        mensal[chave_mes]["receita"] += receita
        mensal[chave_mes]["itens"] += qtd
        mensal[chave_mes]["transacoes"] += 1

        # Produtos
        prod = r["produto"]
        produtos_rev[prod] = produtos_rev.get(prod, 0.0) + receita
        produtos_qtd[prod] = produtos_qtd.get(prod, 0) + qtd

        # Categorias
        cat = r["categoria"]
        categorias_rev[cat] = categorias_rev.get(cat, 0.0) + receita

        # Regiões
        reg = r["regiao"]
        regioes_rev[reg] = regioes_rev.get(reg, 0.0) + receita
        regioes_qtd_transacoes[reg] = regioes_qtd_transacoes.get(reg, 0) + 1

    # Top 5 produtos por receita decrescente
    top_5_produtos = sorted(produtos_rev.items(), key=lambda x: x[1], reverse=True)[:5]

    # Ticket médio regional
    ticket_medio_regional = {
        reg: round(regioes_rev[reg] / regioes_qtd_transacoes[reg], 2)
        for reg in regioes_rev
    }

    media_receita_transacao = receita_global / len(registros) if registros else 0.0
    acima_da_media = sum(1 for r in registros if r["receita_total"] > media_receita_transacao)

    print("\n" + "=" * 50)
    print("=== RF05: RESUMO ANALÍTICO DAS VENDAS ===")
    print("=" * 50)
    print(f"Faturamento Global:     R$ {receita_global:,.2f}")
    print(f"Itens Comercializados:  {itens_globais} unidades")
    print(f"Ticket Médio Global:    R$ {media_receita_transacao:,.2f}")
    print(f"Vendas Acima da Média:  {acima_da_media} transações")
    print("\nTop 5 Produtos por Faturamento:")
    for pos, (produto, valor) in enumerate(top_5_produtos, start=1):
        print(f"  {pos}. {produto}: R$ {valor:,.2f}")

    return {
        "mensal": mensal,
        "top_5_produtos": top_5_produtos,
        "categorias": categorias_rev,
        "regioes": ticket_medio_regional,
        "faturamento_global": round(receita_global, 2),
        "itens_globais": itens_globais,
        "ticket_medio_global": round(media_receita_transacao, 2),
        "transacoes_acima_media": acima_da_media,
    }


if __name__ == "__main__":
    gerar_dataset_vendas()
    dados_brutos = carregar_dataset()
    inspecionar_dados(dados_brutos)
    dados_limpos, relatorio = limpar_dados(dados_brutos)
    dados_enriquecidos = criar_colunas_derivadas(dados_limpos)
    metricas = calcular_metricas(dados_enriquecidos)