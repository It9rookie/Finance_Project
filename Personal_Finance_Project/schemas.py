from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]

class IncomeCreate(BaseModel):
    amount: float
    source: str
    date: Optional[datetime]

class IncomeRead(BaseModel):
    id: int
    amount: float
    source: str
    date: datetime

class IncomeUpdate(BaseModel):
    amount: Optional[float]
    source: Optional[str]
    date: Optional[datetime]

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    date: Optional[datetime]

class ExpenseRead(BaseModel):
    id: int
    amount: float
    category: str
    date: datetime

class ExpenseUpdate(BaseModel):
    amount: Optional[float]
    category: Optional[str]
    date: Optional[datetime]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None