from sqlalchemy import BigInteger, Text, Numeric, ForeignKey, Date, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    full_name: Mapped[str] = mapped_column(Text)
    position: Mapped[str | None] = mapped_column(Text)
    department: Mapped[str | None] = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    customer_name: Mapped[str] = mapped_column(Text)
    amount = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(Text)
    manager_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("employees.id"))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    employee_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("employees.id"))
    status: Mapped[str] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(Text)
    deadline = mapped_column(DateTime(timezone=True))
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("orders.id"))
    product_name: Mapped[str] = mapped_column(Text)
    quantity: Mapped[int]
    total_price = mapped_column(Numeric(12, 2))
    sale_date = mapped_column(Date)


class CommandHistory(Base):
    __tablename__ = "command_history"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    recognized_text: Mapped[str] = mapped_column(Text)
    intent: Mapped[str | None] = mapped_column(Text)
    parameters = mapped_column(JSON)
    result_text: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())