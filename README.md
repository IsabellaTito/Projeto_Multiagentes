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