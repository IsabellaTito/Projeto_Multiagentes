import pandas as pd
import streamlit as st

from shared.repository import ExpenseRepository
from shared.storage import get_db

class SheetPage():

    def __init__(self,session_id:int):
        db = get_db()
        self.expense_repository = ExpenseRepository(db)

        expenses_data = self.expense_repository.get_expenses_data(session_id)

        columns=[
            #"id",
            "data",
            "descricao",
            "categoria",
            "valor",
            "created_at"
        ]

        self.df = pd.DataFrame(expenses_data, columns=columns)

        
    def render(self):
        st.title("Planilha de Gastos")

        if self.df.empty:     
            st.warning("Ainda não há dados para serem exibidos. Converse com o chat e envie seus gastos!")
        else:   
            # Conversão de datas
            self.df["data"] = pd.to_datetime(self.df["data"]).dt.strftime("%d/%m/%Y")
            self.df["created_at"] = pd.to_datetime(self.df["created_at"]).dt.strftime("%d/%m/%Y %H:%M")

            self.df = self.df.rename(columns={
                #"id": "ID",
                "data": "Data",
                "descricao": "Descrição",
                "categoria": "Categoria",
                "valor": "Valor",
                "created_at": "Criado em"
            })

            # Exibição
            st.dataframe(
                self.df,
                width="stretch",
                hide_index=True,
                column_config={
                    "Valor": st.column_config.NumberColumn(
                        "Valor",
                        format="R$ %.2f"
                    )
                }
            )
