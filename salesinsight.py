"""
SalesInsight PY — Análise de Dados de Vendas com Python
Módulo 01 - Escopo Semanas 01 a 05
Etapa 4: RF01 ao RF04 (Dataset, Inspeção, Limpeza e Colunas Derivadas)
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
    """
    Calcula receita total, decompõe a data em partes de calendário
    e classifica a faixa de valor por item unitário com if/elif/else.
    """
    meses_nomes = [
        "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    for r in registros:
        # 1. Receita total da transação
        r["receita_total"] = round(r["quantidade"] * r["preco_unitario"], 2)

        # 2. Decomposição da data
        data: datetime = r["data_venda"]
        r["mes"] = data.month
        r["mes_nome"] = meses_nomes[data.month]
        r["ano"] = data.year

        # 3. Trimestre fiscal
        if data.month <= 3:
            r["trimestre"] = "Q1"
        elif data.month <= 6:
            r["trimestre"] = "Q2"
        elif data.month <= 9:
            r["trimestre"] = "Q3"
        else:
            r["trimestre"] = "Q4"

        # 4. Faixa de valor por preço unitário
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
    if registros:
        print(f"Exemplo de linha enriquecida:\n  {registros[0]}")

    return registros


if __name__ == "__main__":
    gerar_dataset_vendas()
    dados_brutos = carregar_dataset()
    inspecionar_dados(dados_brutos)
    dados_limpos, relatorio = limpar_dados(dados_brutos)
    dados_enriquecidos = criar_colunas_derivadas(dados_limpos)