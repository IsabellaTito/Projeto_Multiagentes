# Projeto Multiagentes

Projeto desenvolvido ao longo da disciplina de Sistemas Multiagentes com o objetivo de por em prática os conhecimentos aprendidos sobre **Agentic AI**.

**Título do projeto:** Financial Agents

O projeto tem como objetivo desenvolver um sistema multiagente que funcione como um assitente financeiro pessoal para registrar e organizar informações de gastos interagindo com o usuário por meio de lingaugem natural.

## Release 1 (28/04/2026)

A primeira release do projeto já entrega um `ChatAgent` criado com **LangChain** para interagir diretamente com o usuário. 
O objetivo deste primeiro agente é receber despesas informadas diretamente pelo usuário, para posteriormente realizar consultas e o próprio sistema multiagente realizar estatísticas acerca do entendimento do padrão de cosumo.

Essa primeira release inclue as seguintes features:
- Protótipo do Frontend com chat para interação com o assitente
- Estrutura inical do banco de dados para persistir mensagens do assistente e do usuário
- Agente de chat implementado com LangChain
- Estrutura para carregar os prompts dos agentes a partir de arquivos `yaml` 

## Como rodar?

Inicie o projeto com o comando:


Inicie o projeto com o comando:
```bash
make init
```

Para rodar faça:

```bash
make app
```