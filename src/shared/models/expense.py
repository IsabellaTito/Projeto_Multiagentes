from datetime import datetime, date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from shared.models import ChatSession


class Expense(BaseModel):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id"), nullable=False, index=True)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    session: Mapped["ChatSession"] = relationship(back_populates="expenses")