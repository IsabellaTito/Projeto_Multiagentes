<div align="center">

# 🤖 Projeto Multiagentes

Projeto desenvolvido ao longo da disciplina de Sistemas Multiagentes com o objetivo de pôr em prática os conhecimentos aprendidos sobre **Agentic AI**.

</div>

<br>

<div align="center">

![Python](https://img.shields.io/badge/python-3.x-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![LangChain](https://img.shields.io/badge/LangChain-Agentic%20AI-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-ff4b4b)
![Pydantic](https://img.shields.io/badge/Pydantic-Validation-009688)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)

</div>

## 💰 Financial Agents

O projeto tem como objetivo desenvolver um sistema multiagente que funcione como um assistente financeiro pessoal para registrar e organizar informações de gastos, interagindo com o usuário por meio de linguagem natural.

---

## Sprint 1 (28/04/2026) 🚀

A primeira sprint do projeto já entrega um `ChatAgent` criado com **LangChain** para interagir diretamente com o usuário.

O objetivo deste primeiro agente é receber despesas informadas diretamente pelo usuário, para posteriormente realizar consultas e permitir que o próprio sistema multiagente gere estatísticas a partir do entendimento do padrão de consumo.

### Features desta sprint

- Protótipo de frontend com chat para interação com o assistente.
- Estrutura inicial do banco de dados para persistência de mensagens do assistente e do usuário.
- Agente de chat implementado com LangChain.
- Estrutura para carregamento de prompts dos agentes a partir de arquivos `yaml`.

---

## Sprint 2 (12/05/2026) 🚀

Neste segundo sprint o `ChatAgent` foi aprimorado, além de interagir com o usuário para receber e organizar as informações sobre os gastos, ele possui uma `tool` que aciona um subagente chamado `ExpenseAgent`. O subagente recebe os dados de um gasto, organiza em um output estruturado (conforme a tabela de gastos) e define uma categoria para o gasto, para posteriormente ser enviado para persisitir no banco de dados. Também foi criada uma página que renderiza uma tabela com os gastos.

### Features desta sprint

- O `ChatAgent` foi aprimorado com uma `tool` que aciona o subagente `ExpenseAgent` e persiste a resposta estruturada para o banco de dados.
- Criação do `ExpenseAgent` que recebe informações de um gasto, define a categoria com base nas informações e cria o output estruturado conforme a tabela de gastos espera.
- Adição de uma página para renderizar uma planilha com os gastos registrados pelos agentes.
- Os dados de gasto e as mensagens do usuário com o `ChatAgent` são persistidos em banco de dados relacional.

### Arquitetura do sistema multiagente nesta sprint

````mermaid
sequenceDiagram
    autonumber
    actor Usuario as Usuário
    participant Chat as ChatAgent
    participant ToolSub as Tool: Chamar Subagente
    participant Expense as ExpenseAgent
    participant DB as Banco SQLite

    Usuario->>Chat: Envia mensagem de despesa
    Chat->>ToolSub: Executa rotina
    ToolSub->>Expense: Aciona Subagente
    Expense->>Expense: Executa Tool (Obter Data)
    Expense->>Expense: Aplica Output Estruturado
    Expense-->>ToolSub: Retorna dados formatados
    ToolSub->>DB: Salva os dados estruturados
    ToolSub-->>Chat: Confirma sucesso
    Chat-->>Usuario: Responde ao usuário

````
---

## Sprint 3 (26/05/2026) 🚀

Nessa terceira sprint, nosso sistema foi aprimorado para receber os gastos não apenas via conversa com o `ChatAgent`, mas também para receber via upload de arquivos. Na aba `uploads`, o usuário pode enviar notas fiscais, recibos, comprovantes, boletos, faturas, entre outros documentos que serão lidos e terão seus dados extraídos pelo novo agente, `DocReaderAgent`. Esse agente extrai os gastos dos documentos enviados de maneira estruturada e persiste esse dados na tabela de gastos. 

Além desse novo agente, foi criada a página de `Dashboard`. A página exibe gráficos com estátisticas dos gastos já enviados pelo usuário, para que ele possa ter um panorama geral dos seus hábitos financeiros, em qual categoria possui mais gastos, quais as suas tendências, entre outros insights interessantes.

Para finalizar essa entrega, ainda foi criada uma classe que herda de `BaseCallbackHandler` para registrar os callbacks, evidenciando as chamadas aos modelos, o uso de `tools` e as atividades dos agentes, permitindo que exista observabilidade no sistema, tudo registrado em um arquivo `.log`.

### Features desta sprint

- Criação do `DocReaderAgent` que lê os arquivos enviados via upload e registra os gastos identificados na planilha
- Criação da página de `Dashboard` com gráficos e estátisticas interessantes sobre os padrões de gastos do usuário
- Observalidade do sistema com a criação de um `log` para ter maior controle sobre as ações dos agentes e dos modelos, facilitando a auditoria dos eventos e a detecção de bugs.
  
---

## Como rodar? ⚙️

Inicie o projeto com o comando:
```bash
make init
```

Defina corretamente as variáveis de ambiente no arquivo `.env` recem criado pelo `make init`.

Para rodar faça:

```bash
make app
```
