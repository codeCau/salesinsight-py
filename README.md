# SalesInsight PY — Análise de Dados de Vendas com Python

Projeto desenvolvido como parte da avaliação do **Módulo 01 (Semanas 01 a 05)** da formação em Desenvolvimento em IA para Análise Preditiva. A aplicação consiste em um pipeline completo de análise de dados de varejo construído exclusivamente com a **biblioteca padrão do Python**, sem dependências externas.

---

## 📌 Sobre o Projeto

O **SalesInsight PY** simula o fluxo de trabalho de um Analista de Dados Júnior em uma empresa varejista. A ferramenta carrega um histórico bruto de transações comerciais, inspeciona e remove dados inconsistentes, realiza transformações e derivações condicionais, agrega os indicadores financeiros em diferentes dimensões de negócio e exporta os resultados estruturados em formatos relacionais (CSV) e semiestruturados (JSON).

---

## 📊 O que o Projeto Analisa

- **Evolução Temporal:** Faturamento bruto, volume total de itens e quantidade de transações agrupados por mês e classificados por trimestre (Q1 a Q4).
- **Desempenho Comercial:** Ranqueamento de *Top 5 Produtos* e faturamento acumulado por categoria de item.
- **Eficiência Regional:** Receita agregada e cálculo de ticket médio transacional por região geográfica.
- **Segmentação de Clientes:** Categorização da carteira em *Bronze* (até R$ 5.000,00), *Prata* (R$ 5.000,00 a R$ 15.000,00) e *Ouro* (acima de R$ 15.000,00) a partir do volume financeiro individual acumulado.
- **Transações Acima da Média:** Identificação do quantitativo de vendas individuais cujo valor total superou a média geral da base de dados.
- **Exportação Analítica:** Geração automatizada de relatórios em CSV e sumário consolidado em JSON.

---

## 🧠 Conceitos Aplicados (Módulo 01 — Semanas 01 a 05)

- **Lógica e Controle de Fluxo:** Variáveis com tipagem dinâmica, operadores aritméticos/relacionais e estruturas de repetição (`for`).
- **Condicionais e Regras de Negócio:** Aplicação de `if/elif/else` para cálculo dos trimestres e atribuição de faixas de valor (*Baixo Valor*, *Médio Valor*, *Alto Valor*).
- **Estruturas de Dados Compostas:** Modelagem e manipulação intensiva de listas de dicionários (`list[dict]`) para estruturação das tabelas e métricas.
- **Tratamento de Strings e Expressões Regulares:** Remoção de ruído textual e caracteres especiais com `re.sub()`, além de validação formal de identificadores com `re.compile()`.
- **Manipulação Temporal:** Uso do módulo nativo `datetime` e do método `strptime()` para parsing seguro e extração de atributos de calendário (`month`, `year`).
- **Programação Funcional e Modularidade:**
  - Funções com escopo delimitado, parâmetros explícitos, retornos padronizados e documentação via *docstrings*.
  - Funções de ordem superior (`processar_coluna`), passando funções como argumentos de transformação.
  - Funções anônimas (`lambda`) aplicadas na segmentação de clientes e em chaves de ordenação com `sorted()`.
- **Persistência e Leitura de Arquivos:** Módulos `csv` (`DictReader`, `DictWriter`) e `json` (`dump`, `load`) com validação imediata em memória dos dados exportados.
- **Boas Práticas de Engenharia:** Modularização em torno de uma função `main()` orquestradora e proteção de execução via bloco `if __name__ == "__main__":`.

---

## 🛠️ Decisões Técnicas de Implementação

1. **Descarte Crítico vs. Imputação de Nulos (RF03):**
   Optou-se pela exclusão direta de registros que apresentavam campos nulos em `quantidade` ou `preco_unitario`, bem como transações com datas corrompidas (`DATA INVALIDA`). Como o escopo do Módulo 01 não abrange técnicas estatísticas de imputação (médias, medianas ou regressões), qualquer preenchimento arbitrário introduziria viés artificial ao ticket médio regional e distorções sazonais nos relatórios mensais.
2. **Agregação Única em Dicionários Nativos (RF05 e RF06):**
   Para evitar múltiplos loops aninhados com custo computacional O(n²), o processamento de agregação foi implementado com dicionários acumuladores em uma única iteração O(n). Essa abordagem garante performance eficiente mesmo sem a utilização de bibliotecas otimizadas como Pandas.
3. **Garantia de Encoding UTF-8 com BOM nos CSVs (RF08):**
   A exportação dos relatórios foi configurada com o encoding `utf-8-sig`. Esse padrão assegura compatibilidade imediata com ferramentas analíticas externas (como o Microsoft Excel), preservando a acentuação correta de textos em português sem corrupção de caracteres.

---

## 📁 Estrutura do Projeto

```text
salesinsight-py/
├── salesinsight.py                 # Script orquestrador do pipeline analítico
├── vendas.csv                      # Dataset bruto gerado ou carregado
├── README.md                       # Documentação completa e instruções
├── outputs/                        # Diretório criado em tempo de execução
│   ├── metricas_por_mes.csv        # Consolidado mensal de receitas e volumes
│   ├── segmentacao_clientes.csv    # Carteira de clientes classificada (Bronze/Prata/Ouro)
│   ├── estatisticas_gerais.json    # Indicadores globais da base higienizada
├── planejamento/
    └── kanban-salesinsight-py.md          # Registro da organização e backlog do projeto
```

---

## 🚀 Como Executar

O projeto utiliza exclusivamente bibliotecas built-in do Python, dispensando a instalação de qualquer dependência via `pip`.

### Execução Local (VS Code ou Terminal)

1. Certifique-se de possuir o **Python 3.10 ou superior** instalado.
2. Clone o repositório ou baixe os arquivos em uma pasta de trabalho:
   ```bash
   git clone https://github.com/codeCau/salesinsight-py.git
   cd salesinsight-py
   ```
3. Execute o script principal:
   ```bash
   python salesinsight.py
   ```
4. O script verificará a existência do arquivo `vendas.csv`. Caso ausente, ele gerará automaticamente uma base sintética com 200 registros contendo as inconsistências controladas, executará o pipeline e criará a pasta `outputs/`.

### Execução no Google Colab

1. Abra um novo notebook no Google Colab.
2. Faça upload do arquivo `salesinsight.py` na aba lateral de arquivos.
3. Em uma célula de código, execute:
   ```python
   !python salesinsight.py
   ```
4. Atualize a listagem de arquivos para visualizar a pasta `outputs/` e baixar os relatórios.

---

## 🔧 Ferramentas Utilizadas

- **Linguagem:** Python 3.10+
- **Bibliotecas Empregadas:** `csv`, `json`, `re`, `datetime`, `os`, `random`
- **Ambientes de Desenvolvimento:** VS Code
- **Versionamento:** Git e GitHub (seguindo o padrão *Conventional Commits* e branches por funcionalidade)
- **Gestão de Tarefas (Kanban):** Markdown local (`planejamento/kanban-salesinsight-py.md`)

---

## 📹 Vídeo de Demonstração

Assista à apresentação do projeto abordando o objetivo de negócio, a arquitetura do código, as justificativas técnicas e a demonstração do pipeline rodando do início ao fim:

- **Link do Vídeo:** [Clique aqui para assistir]()