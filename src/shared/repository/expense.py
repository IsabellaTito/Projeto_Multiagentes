from datetime import date
from decimal import Decimal

from shared.enums import ExpenseCategory
from shared.models import Expense
from shared.storage.database import Database


class ExpenseRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_expense(
        self,
        session_id: int,
        data: date,
        descricao: str,
        categoria: ExpenseCategory,
        valor: Decimal
    ) -> Expense:
        with self.db.session_scope() as session:
            expense = Expense(
                session_id=session_id,
                data=data,
                descricao=descricao,
                categoria=categoria.value,
                valor=valor
            )

            session.add(expense)
            session.flush()

            return expense

    def get_expense_by_id(self, expense_id: int) -> Expense | None:
        with self.db.session_scope() as session:
            return session.get(Expense, expense_id)

    def get_expenses_by_session(self, session_id: int):
        with self.db.session_scope() as session:
            return (
                session.query(Expense)
                .filter(Expense.session_id == session_id)
                .order_by(Expense.data.desc())
                .all()
            )

    def get_all_expenses(self):
        with self.db.session_scope() as session:
            return (
                session.query(Expense)
                .order_by(Expense.created_at.desc())
                .all()
            )

    def delete_expense(self, expense_id: int) -> bool:
        with self.db.session_scope() as session:
            expense = session.get(Expense, expense_id)

            if not expense:
                return False

            session.delete(expense)

            return True

    def update_expense(
        self,
        expense_id: int,
        *,
        data: date | None = None,
        descricao: str | None = None,
        categoria: ExpenseCategory | None = None,
        valor: Decimal | None = None
    ) -> Expense | None:
        with self.db.session_scope() as session:
            expense = session.get(Expense, expense_id)

            if not expense:
                return None

            if data is not None:
                expense.data = data

            if descricao is not None:
                expense.descricao = descricao

            if categoria is not None:
                expense.categoria = categoria.value

            if valor is not None:
                expense.valor = valor

            session.flush()

            return expense

    def get_expenses_data(self, session_id: int) -> list[dict]:
        with self.db.session_scope() as session:
            expenses = (
                session.query(Expense)
                .where(Expense.session_id == session_id)
                .order_by(Expense.data.desc())
                .all()
            )

            return [
                {
                    "id": expense.id,
                    "data": expense.data,
                    "descricao": expense.descricao,
                    "categoria": expense.categoria,
                    "valor": float(expense.valor),
                    "created_at": expense.created_at
                }
                for expense in expenses
            ]

    def get_expenses(
        self,
        *,
        session_id: int,
        data: date | None = None,
        descricao: str | None = None,
        categoria: ExpenseCategory | None = None,
    ) -> list[Expense]:
        with self.db.session_scope() as session:
            query = session.query(Expense)
            query = query.filter(Expense.session_id == session_id)

            if data is not None:
                query = query.filter(Expense.data == data)

            if descricao:
                query = query.filter(Expense.descricao.ilike(f"%{descricao}%"))

            if categoria is not None:
                query = query.filter(Expense.categoria == categoria.value)

            expenses = (
                query
                .order_by(Expense.data.desc())
                .all()
            )

            return [
            {
                "id": e.id,
                "data": e.data.isoformat(),
                "descricao": e.descricao,
                "categoria": e.categoria,
                "valor": float(e.valor),
            }
            for e in expenses
        ]