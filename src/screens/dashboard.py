import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from shared.repository import ExpenseRepository
from shared.storage import get_db

class DashboardPage:

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

        # Garantir tipos corretos
        self.df["data"] = pd.to_datetime(self.df["data"])
        self.df["valor"] = pd.to_numeric(self.df["valor"])

    def render(self):

        st.title("Dashboard Financeiro")

        if self.df.empty:
            st.warning("Nenhuma despesa registrada.")
            return

        # ==================================================
        # MÉTRICAS
        # ==================================================

        total_gastos = self.df["valor"].sum()

        categoria_maior_gasto = (
        self.df.groupby("categoria")["valor"]
            .sum()
            .sort_values(ascending=False)
        )

        if not categoria_maior_gasto.empty:
            top_categoria = categoria_maior_gasto.index[0]
            top_categoria_valor = categoria_maior_gasto.iloc[0]
        else:
            top_categoria = "-"
            top_categoria_valor = 0

        data_com_mais_gastos = (
            self.df.groupby(self.df["data"].dt.date)
            .size()
            .sort_values(ascending=False)
        )

        if not data_com_mais_gastos.empty:
            top_data = data_com_mais_gastos.index[0]
            top_data_qtd = data_com_mais_gastos.iloc[0]
        else:
            top_data = "-"
            top_data_qtd = 0

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="💰 Total de Gastos",
                value=f"R$ {total_gastos:,.2f}",
                border=True,
                help="Somatório total dos gastos desde que o agente começou os registrar"
            )

        with col2:
            st.metric(
                label="📊 Categoria com Maior Gasto",
                value=top_categoria,
                delta=f"R$ {top_categoria_valor:,.2f}",
                border=True,
                help="Categoria que registrou maiores gastos"
            )

        with col3:
            st.metric(
                label="📅 Dia com Mais Gastos",
                value=top_data.strftime("%d/%m/%Y"),
                delta=f"{top_data_qtd} gastos",
                border=True,
                help="Dia no qual houve maior ocorrencia de gastos",
            )

        # ==================================================
        # GRÁFICOS
        # ==================================================

        col_graf1, col_graf2 = st.columns(2)

        # --------------------------------------------------
        # GASTOS POR CATEGORIA
        # --------------------------------------------------

        with col_graf1:

            st.subheader("Gastos por Categoria")

            gastos_categoria = (
                self.df.groupby("categoria")["valor"]
                .sum()
                .reset_index()
                .sort_values(by="valor", ascending=False)
            )

            fig1 = px.bar(
                gastos_categoria,
                x="categoria",
                y="valor",
                title="",
                labels={
                    "categoria": "Categoria",
                    "valor": "Valor"
                }
            )

            st.container(border=True).plotly_chart(fig1, width='stretch')

        # --------------------------------------------------
        # DISTRIBUIÇÃO DOS GASTOS
        # --------------------------------------------------

        with col_graf2:

            st.subheader("Distribuição dos Gastos")

            qtd_categoria = (
                self.df.groupby("categoria")["valor"]
                .sum()
                .reset_index()
            )

            fig2 = px.pie(
                qtd_categoria,
                names="categoria",
                values="valor",
                title=""
            )

            st.container(border=True).plotly_chart(fig2, width='stretch')

        # ==================================================
        # EVOLUÇÃO DOS GASTOS
        # ==================================================

        st.subheader("Gastos ao Longo do Tempo")

        gastos_por_data = (
            self.df.groupby(self.df["data"].dt.date)["valor"]
            .sum()
            .reset_index()
        )

        fig3 = px.line(
            gastos_por_data,
            x="data",
            y="valor",
            title="",
            markers=True,
            labels={
                "data": "Data",
                "valor": "Valor"
            }
        )

        st.container(border=True).plotly_chart(
            fig3,
            width='stretch'
        )


        # ==================================================
        # QUANTIDADE DE GASTOS POR DIA
        # ==================================================

        st.subheader("Quantidade de Gastos por Dia")

        qtd_por_data = (
            self.df.groupby(self.df["data"].dt.date)
            .size()
            .reset_index(name="quantidade")
        )

        fig4 = px.bar(
            qtd_por_data,
            x="data",
            y="quantidade",
            title="",
            labels={
                "data": "Data",
                "quantidade": "Quantidade"
            }
        )

        st.container(border=True).plotly_chart(
            fig4,
            width='stretch'
        )

        # ==================================================
        # MAIORES GASTOS
        # ==================================================

        st.subheader("Maiores Gastos")

        maiores_gastos = (
            self.df.sort_values(by="valor", ascending=False)
            .head(10)
        )

        st.dataframe(
            maiores_gastos,
            width='stretch',
            hide_index=True,
            column_config={
                    "valor": st.column_config.NumberColumn(
                        "valor",
                        format="R$ %.2f",
                        alignment="left"
                    )
                }
        )
