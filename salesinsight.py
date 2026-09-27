"""
SalesInsight PY — Análise de Dados de Vendas com Python
Módulo 01 - Escopo Semanas 01 a 05
Etapa 1: RF01 (Geração/Carga) e RF02 (Inspeção Estrutural)
"""

import csv
import random
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

            # Sujeiras propositais para testar a etapa de limpeza
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

    print(f"[RF01] Dataset gerado com {n_registros} registros em '{caminho_csv}'.")


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
    print(f"Colunas identificadas: {colunas}")
    print(f"Valores ausentes por coluna:\n{nulos}")
    print("\nPrimeiros registros brutos:")
    for linha in registros[:3]:
        print(f"  {linha}")
    return registros


if __name__ == "__main__":
    gerar_dataset_vendas()
    dados_brutos = carregar_dataset()
    inspecionar_dados(dados_brutos)