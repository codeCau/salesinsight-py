# Quadro Kanban — SalesInsight PY

Quadro de acompanhamento das tarefas do mini-projeto avaliativo (Módulo 01 - Semanas 01 a 05).

## 📋 Backlog / A Fazer

- [ ] Implementar bônus B02: Projeção de tendência com média móvel (Opcional)
- [ ] Adicionar testes unitários com `unittest` para a função de limpeza (Melhoria futura)

## ⚙️ Em Andamento

*(Nenhuma tarefa em andamento no momento)*

## ✅ Concluído

### Sprint 1: Setup e Planejamento

- [x] **Configuração Inicial do Repositório**: Inicialização do Git, branches `main` e `develop`, `.gitignore`.
- [x] **Estruturação do Kanban**: Definição das entregas e critérios de aceitação.
- [x] **README Inicial**: Esboço dos objetivos e tecnologias utilizadas (`docs/readme`).

### Sprint 2: Engenharia e Limpeza de Dados (RF01 a RF03)

- [x] **RF01 - Geração/Carga do Dataset**: Criação da função `gerar_dataset_vendas()` com dados sintéticos sujos e função `carregar_dataset()`.
- [x] **RF02 - Inspeção Estrutural**: Implementação de `inspecionar_dados()` com contagem de nulos e primeiras linhas.
- [x] **RF03 - Limpeza e Sanitização**: Tratamento de espaços com `.strip()`, validação de datas com `datetime.strptime`, descarte de nulos críticos e higienização de clientes com `re.sub()`.

### Sprint 3: Transformação e Métricas (RF04 a RF07)

- [x] **RF04 - Colunas Derivadas**: Criação de `receita_total`, decomposição de data (`mes`, `mes_nome`, `ano`, `trimestre`) e faixas condicionais (`faixa_receita_item`).
- [x] **RF05 - Agregações Analíticas**: Cálculo de receita mensal, Top 5 produtos, faturamento por categoria e ticket médio regional via dicionários acumuladores.
- [x] **RF06 - Segmentação de Clientes**: Agrupamento de gastos por cliente e classificação em Bronze/Prata/Ouro utilizando expressão `lambda`.
- [x] **RF07 - Função de Ordem Superior**: Implementação de `processar_coluna()` recebendo lambdas para enriquecimento de dados.

### Sprint 4: Exportação e Entrega (RF08 a RF11 + Docs)

- [x] **RF08 - Persistência de Dados**: Exportação em CSV com `csv.DictWriter` (encoding UTF-8 com BOM) e estatísticas em JSON com `json.dump` / conferência via `json.load`.
- [x] **RF09 - Orquestração Main**: Ponto de entrada com fluxo completo sob `if __name__ == "__main__":`.
- [x] **Documentação Final**: README.md atualizado com justificativas técnicas e instruções de execução.
- [x] **Vídeo Demonstrativo**: Gravação de até 5 minutos abordando decisões técnicas, ambiente e execução.

### Opção 2: Se preferir criar visualmente no GitHub Projects

Se quiser a interface gráfica de cartões para mostrar no vídeo de 5 minutos, siga estes 4 passos:

1. Acesse o seu repositório no GitHub pelo navegador.
2. Clique na aba superior **Projects** → botão verde **New project** → selecione o template **Board** e clique em **Create**.
3. O GitHub criará 3 colunas padrão: **Todo** (A Fazer), **In Progress** (Em Andamento) e **Done** (Concluído).
4. No rodapé da coluna **Done**, clique em `+ Add item` e crie 5 cartões rápidos:
   - `[RF01/RF02] Carga e inspeção estrutural de dados`
   - `[RF03] Limpeza de nulos, datetime e regex`
   - `[RF04/RF05] Colunas derivadas e agregações analíticas`
   - `[RF06/RF07] Segmentação com lambda e ordem superior`
   - `[RF08/RF09] Exportação CSV/JSON e pipeline main()`

Ao gravar o vídeo, você pode abrir essa tela do GitHub Projects por 15 segundos e dizer: *"Aqui está o quadro Kanban onde mapeei cada requisito funcional em cartões antes de iniciar o desenvolvimento."*
