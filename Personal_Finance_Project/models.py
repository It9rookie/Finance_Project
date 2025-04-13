from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    incomes: List["Income"] = Relationship(back_populates="user")
    expenses: List["Expense"] = Relationship(back_populates="user")

class Income(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    amount: float
    source: str
    date: datetime = Field(default=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="incomes")

class Expense(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    amount: float
    category: str
    date: datetime = Field(default=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="expenses")