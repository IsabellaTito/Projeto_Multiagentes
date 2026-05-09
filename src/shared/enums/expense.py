from enum import StrEnum

class ExpenseCategory(StrEnum):
    ALIMENTACAO = "Alimentação"
    TRANSPORTE = "Transporte"
    MORADIA = "Moradia"
    SAUDE = "Saúde"
    EDUCACAO = "Educação"
    LAZER = "Lazer"
    MERCADO = "Mercado"
    CONTAS = "Contas"
    OUTROS = "Outros"