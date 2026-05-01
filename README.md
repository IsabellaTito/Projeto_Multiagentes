# Projeto Multiagentes 🤖

![Python](https://img.shields.io/badge/python-3.x-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)
![LangChain](https://img.shields.io/badge/LangChain-Agentic%20AI-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-ff4b4b)

Projeto desenvolvido ao longo da disciplina de Sistemas Multiagentes com o objetivo de pôr em prática os conhecimentos aprendidos sobre **Agentic AI**.

**Título do projeto:** Financial Agents 💰

O projeto tem como objetivo desenvolver um sistema multiagente que funcione como um assistente financeiro pessoal para registrar e organizar informações de gastos, interagindo com o usuário por meio de linguagem natural.

## Release 1 (28/04/2026) 🚀

A primeira release do projeto já entrega um `ChatAgent` criado com **LangChain** para interagir diretamente com o usuário.

O objetivo deste primeiro agente é receber despesas informadas diretamente pelo usuário, para posteriormente realizar consultas e permitir que o próprio sistema multiagente gere estatísticas a partir do entendimento do padrão de consumo.

### Features desta release ✨

- Protótipo de frontend com chat para interação com o assistente  
- Estrutura inicial do banco de dados para persistência de mensagens do assistente e do usuário  
- Agente de chat implementado com LangChain  
- Estrutura para carregamento de prompts dos agentes a partir de arquivos `yaml`  

## Como rodar? ⚙️

Inicie o projeto com o comando:
```bash
make init
```

Para rodar faça:

```bash
make app
```