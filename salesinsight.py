"""
SalesInsight PY — Análise de Dados de Vendas com Python
Módulo 01 - Escopo Semanas 01 a 05
Pipeline analítico completo (RF01 ao RF09) utilizando apenas biblioteca padrão.
"""

import csv
import json
import os
import random
import re
from datetime import datetime, timedelta


# ==========================================
# RF01 - GERAÇÃO E CARGA DO DATASET
# ==========================================
def gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42):
    """
    Gera um dataset sintético de vendas no varejo contendo inconsistências
    controladas para simulação do pipeline e salva em formato CSV.
    """
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

            # Injeção controlada de inconsistências
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

    print(f"[RF01] Dataset gerado com sucesso: '{caminho_csv}' ({n_registros} registros).")


def carregar_dataset(caminho_csv="vendas.csv"):
    """Lê o arquivo CSV bruto e retorna uma lista de dicionários."""
    with open(caminho_csv, "r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        return list(leitor)


# ==========================================
# RF02 - INSPEÇÃO DOS DADOS BRUTOS
# ==========================================
def inspecionar_dados(registros):
    """
    Exibe a contagem total de linhas, colunas existentes e quantidade
    de valores nulos/vazios em cada atributo.
    """
    total = len(registros)
    colunas = list(registros[0].keys()) if registros else []
    nulos = {col: 0 for col in colunas}

    for linha in registros:
        for col in colunas:
            if linha.get(col, "").strip() == "":
                nulos[col] += 1

    print("\n" + "=" * 55)
    print("=== RF02: INSPEÇÃO ESTRUTURAL DO DATASET ===")
    print("=" * 55)
    print(f"Total de registros: {total}")
    print(f"Colunas presentes: {colunas}")
    print(f"Valores ausentes por coluna:\n{nulos}")
    return registros


# ==========================================
# RF03 - LIMPEZA E SANITIZAÇÃO DOS DADOS
# ==========================================
def limpar_dados(registros):
    """
    Higieniza textos com strip, valida e converte datas via datetime,
    descarta registros corrompidos, converte numéricos e sanitiza clientes com regex.
    """
    relatorio = {
        "iniciais": len(registros),
        "removidos_data": 0,
        "removidos_nulos": 0,
        "finais": 0
    }
    padrao_cliente = re.compile(r"^Cliente_\d{3}$", flags=re.IGNORECASE)
    limpos = []

    for linha in registros:
        # Remoção de espaços em branco nas pontas
        for campo in ("cliente", "produto", "categoria", "regiao"):
            linha[campo] = linha[campo].strip()

        # Validação temporal
        try:
            linha["data_venda"] = datetime.strptime(linha["data_venda"], "%Y-%m-%d")
        except ValueError:
            relatorio["removidos_data"] += 1
            continue

        # Descarte de nulos críticos em quantidade e preço
        if linha["quantidade"] == "" or linha["preco_unitario"] == "":
            relatorio["removidos_nulos"] += 1
            continue

        # Conversão de tipos primitivos
        linha["quantidade"] = int(float(linha["quantidade"]))
        linha["preco_unitario"] = float(linha["preco_unitario"])

        # Higienização de strings com regex
        nome_limpo = re.sub(r"[^A-Za-z0-9_]", "", linha["cliente"])
        linha["cliente"] = nome_limpo
        linha["cliente_fora_do_padrao"] = padrao_cliente.match(nome_limpo) is None

        limpos.append(linha)

    relatorio["finais"] = len(limpos)

    print("\n" + "=" * 55)
    print("=== RF03: RELATÓRIO DE HIGIENIZAÇÃO ===")
    print("=" * 55)
    print(f"Registros iniciais:     {relatorio['iniciais']}")
    print(f"Descarte por data:      {relatorio['removidos_data']}")
    print(f"Descarte por nulos:     {relatorio['removidos_nulos']}")
    print(f"Registros validados:    {relatorio['finais']}")

    return limpos, relatorio


# ==========================================
# RF04 - CRIAÇÃO DE COLUNAS DERIVADAS
# ==========================================
def criar_colunas_derivadas(registros):
    """
    Calcula o faturamento da transação, decompõe elementos de data
    e categoriza a faixa de preço unitário utilizando condicionais.
    """
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

    print("\n" + "=" * 55)
    print("=== RF04: COLUNAS DERIVADAS CRIADAS ===")
    print("=" * 55)
    print("Colunas adicionadas: receita_total, mes, mes_nome, ano, trimestre, faixa_receita_item")

    return registros


# ==========================================
# RF05 - CÁLCULO DE MÉTRICAS ANALÍTICAS
# ==========================================
def calcular_metricas(registros):
    """
    Calcula agregações de faturamento temporal, ranqueamento de produtos,
    categorias e ticket médio regional em passada única O(n).
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

        if chave_mes not in mensal:
            mensal[chave_mes] = {"receita": 0.0, "itens": 0, "transacoes": 0}
        mensal[chave_mes]["receita"] += receita
        mensal[chave_mes]["itens"] += qtd
        mensal[chave_mes]["transacoes"] += 1

        prod = r["produto"]
        produtos_rev[prod] = produtos_rev.get(prod, 0.0) + receita
        produtos_qtd[prod] = produtos_qtd.get(prod, 0) + qtd

        cat = r["categoria"]
        categorias_rev[cat] = categorias_rev.get(cat, 0.0) + receita

        reg = r["regiao"]
        regioes_rev[reg] = regioes_rev.get(reg, 0.0) + receita
        regioes_qtd_transacoes[reg] = regioes_qtd_transacoes.get(reg, 0) + 1

    top_5_produtos = sorted(produtos_rev.items(), key=lambda x: x[1], reverse=True)[:5]

    ticket_medio_regional = {
        reg: round(regioes_rev[reg] / regioes_qtd_transacoes[reg], 2)
        for reg in regioes_rev
    }

    media_receita_transacao = receita_global / len(registros) if registros else 0.0
    acima_da_media = sum(1 for r in registros if r["receita_total"] > media_receita_transacao)

    print("\n" + "=" * 55)
    print("=== RF05: RESUMO ANALÍTICO DAS VENDAS ===")
    print("=" * 55)
    print(f"Faturamento Global:     R$ {receita_global:,.2f}")
    print(f"Total Itens Vendidos:   {itens_globais} unidades")
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


# ==========================================
# RF06 - SEGMENTAÇÃO DE CARTEIRA DE CLIENTES
# ==========================================
def segmentar_clientes(registros):
    """
    Agrupa o consumo financeiro acumulado por cliente e classifica a carteira
    em Bronze, Prata e Ouro utilizando uma expressão lambda.
    """
    gastos_clientes = {}
    for r in registros:
        cli = r["cliente"]
        gastos_clientes[cli] = gastos_clientes.get(cli, 0.0) + r["receita_total"]

    classificar_segmento = lambda gasto: (
        "Ouro" if gasto > 15000 else ("Prata" if gasto >= 5000 else "Bronze")
    )

    clientes_segmentados = []
    for cliente, gasto_total in gastos_clientes.items():
        clientes_segmentados.append({
            "cliente": cliente,
            "total_gasto": round(gasto_total, 2),
            "segmento": classificar_segmento(gasto_total)
        })

    clientes_segmentados.sort(key=lambda c: c["total_gasto"], reverse=True)

    contagem_segmentos = {"Bronze": 0, "Prata": 0, "Ouro": 0}
    for c in clientes_segmentados:
        contagem_segmentos[c["segmento"]] += 1

    print("\n" + "=" * 55)
    print("=== RF06: SEGMENTAÇÃO DE CARTEIRA ===")
    print("=" * 55)
    print(f"Clientes únicos identificados: {len(clientes_segmentados)}")
    print(f"Distribuição de carteira:     {contagem_segmentos}")

    return clientes_segmentados


# ==========================================
# RF07 - FUNÇÃO DE ORDEM SUPERIOR
# ==========================================
def processar_coluna(registros, coluna_origem, coluna_destino, funcao_transformacao):
    """
    Função de ordem superior que recebe registros, nome da coluna de origem,
    nome da nova coluna de destino e uma função/lambda de transformação para aplicar
    elemento a elemento.
    """
    for r in registros:
        if coluna_origem in r:
            r[coluna_destino] = funcao_transformacao(r[coluna_origem])
    return registros


# ==========================================
# RF08 - EXPORTAÇÃO CSV E JSON COM VALIDAÇÃO
# ==========================================
def exportar_resultados(metricas, clientes_segmentados, pasta_saida="outputs"):
    """
    Exporta relatórios analíticos em CSV (com UTF-8-sig) e o resumo em JSON,
    validando a integridade estrutural do arquivo JSON através de json.load().
    """
    os.makedirs(pasta_saida, exist_ok=True)

    # 1. Exportação: metricas_por_mes.csv
    caminho_mes = os.path.join(pasta_saida, "metricas_por_mes.csv")
    with open(caminho_mes, "w", newline="", encoding="utf-8-sig") as f:
        campos = ["ano", "mes", "mes_nome", "trimestre", "receita_total", "itens_vendidos", "total_transacoes"]
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()

        meses_ordenados = sorted(metricas["mensal"].keys(), key=lambda x: (x[0], x[1]))
        for chave in meses_ordenados:
            dados_m = metricas["mensal"][chave]
            escritor.writerow({
                "ano": chave[0],
                "mes": chave[1],
                "mes_nome": chave[2],
                "trimestre": chave[3],
                "receita_total": round(dados_m["receita"], 2),
                "itens_vendidos": dados_m["itens"],
                "total_transacoes": dados_m["transacoes"]
            })

    # 2. Exportação: segmentacao_clientes.csv
    caminho_clientes = os.path.join(pasta_saida, "segmentacao_clientes.csv")
    with open(caminho_clientes, "w", newline="", encoding="utf-8-sig") as f:
        campos_cli = ["cliente", "total_gasto", "segmento"]
        escritor = csv.DictWriter(f, fieldnames=campos_cli)
        escritor.writeheader()
        for cli in clientes_segmentados:
            escritor.writerow(cli)

    # 3. Exportação: estatisticas_gerais.json
    caminho_json = os.path.join(pasta_saida, "estatisticas_gerais.json")
    dados_json = {
        "faturamento_global": metricas["faturamento_global"],
        "itens_globais": metricas["itens_globais"],
        "ticket_medio_global": metricas["ticket_medio_global"],
        "transacoes_acima_media": metricas["transacoes_acima_media"],
        "top_5_produtos": [
            {"produto": prod, "receita": round(val, 2)}
            for prod, val in metricas["top_5_produtos"]
        ],
        "receita_por_categoria": {
            cat: round(val, 2) for cat, val in metricas["categorias"].items()
        },
        "ticket_medio_regional": metricas["regioes"]
    }

    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(dados_json, f, indent=2, ensure_ascii=False)

    # Validação imediata de integridade via leitura com json.load
    with open(caminho_json, "r", encoding="utf-8") as f:
        conferido = json.load(f)

    print("\n" + "=" * 55)
    print("=== RF08: EXPORTAÇÃO E PERSISTÊNCIA ===")
    print("=" * 55)
    print(f"Exportado: {caminho_mes}")
    print(f"Exportado: {caminho_clientes}")
    print(f"Exportado: {caminho_json}")
    print(f"Validação JSON (Leitura OK): Faturamento conferido = R$ {conferido['faturamento_global']:,.2f}")


# ==========================================
# RF09 - ORQUESTRAÇÃO DO PIPELINE (MAIN)
# ==========================================
def main():
    """Ponto de entrada central do pipeline analítico SalesInsight PY."""
    print("Iniciando pipeline analítico SalesInsight PY...\n")

    # 1. Garante existência do dataset inicial
    if not os.path.exists("vendas.csv"):
        gerar_dataset_vendas("vendas.csv")

    # 2. Ingestão e Inspeção
    dados_brutos = carregar_dataset("vendas.csv")
    inspecionar_dados(dados_brutos)

    # 3. Limpeza e Higienização
    dados_limpos, _ = limpar_dados(dados_brutos)

    # 4. Transformação e Derivação de Atributos
    dados_enriquecidos = criar_colunas_derivadas(dados_limpos)

    # 5. Aplicação da Função de Ordem Superior (RF07)
    processar_coluna(
        dados_enriquecidos,
        coluna_origem="receita_total",
        coluna_destino="receita_formatada",
        funcao_transformacao=lambda v: f"R$ {v:,.2f}"
    )

    # 6. Agregações Analíticas e Segmentação
    metricas = calcular_metricas(dados_enriquecidos)
    clientes_segmentados = segmentar_clientes(dados_enriquecidos)

    # 7. Persistência em disco (RF08)
    exportar_resultados(metricas, clientes_segmentados, pasta_saida="outputs")

    print("\n" + "=" * 55)
    print(">>> PIPELINE EXECUTADO COM SUCESSO DE PONTA A PONTA! <<<")
    print("=" * 55)


if __name__ == "__main__":
    main()