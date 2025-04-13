from sqlmodel import Session, select
from models import User, Income, Expense
from schemas import UserCreate, IncomeCreate, ExpenseCreate


def create_user(session: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # 这里先不处理密码哈希，你可以根据实际情况完善
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(session: Session, user_id: int):
    return session.get(User, user_id)


def get_all_users(session: Session):
    statement = select(User)
    return session.exec(statement).all()


def create_income(session: Session, income: IncomeCreate, user_id: int):
    db_income = Income(**income.dict(), user_id=user_id)
    session.add(db_income)
    session.commit()
    session.refresh(db_income)
    return db_income


def get_incomes(session: Session, user_id: int):
    statement = select(Income).where(Income.user_id == user_id)
    return session.exec(statement).all()


def create_expense(session: Session, expense: ExpenseCreate, user_id: int):
    db_expense = Expense(**expense.dict(), user_id=user_id)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return db_expense


def get_expenses(session: Session, user_id: int):
    statement = select(Expense).where(Expense.user_id == user_id)
    return session.exec(statement).all()