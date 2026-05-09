from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from shared.enums import ExpenseCategory


class ExpenseSchema(BaseModel):
    data: date = Field(
        description="Data do gasto"
    )

    descricao: str = Field(
        description="Descrição da compra ou gasto"
    )

    categoria: ExpenseCategory = Field(
        description="Categoria da despesa"
    )

    valor: Decimal = Field(
        description="Valor do gasto"
    )