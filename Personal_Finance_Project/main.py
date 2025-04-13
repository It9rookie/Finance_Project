from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, SQLModel, create_engine
from models import User, Income, Expense
from schemas import UserCreate, UserRead, IncomeCreate, IncomeRead, ExpenseCreate, ExpenseRead, Token, TokenData
from crud import create_user, get_user, create_income, get_incomes, create_expense, get_expenses, get_all_users
from auth import authenticate_user, create_access_token, get_current_user
from database import engine, create_db_and_tables
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/register", response_class=HTMLResponse)
def show_register_page():
    html_content = """
    <html>
        <body>
            <h1>Register Page</h1>
            <form method="post" action="/register">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" required><br>
                <label for="email">Email:</label><br>
                <input type="email" id="email" name="email" required><br>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="Register">
            </form>
        </body>
    </html>
    """
    return html_content


@app.get("/login", response_class=HTMLResponse)
def show_login_page():
    html_content = """
    <html>
        <body>
            <h1>Login Page</h1>
            <form method="post" action="/login">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" required><br>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password" required><br><br>
                <input type="submit" value="Login">
            </form>
        </body>
    </html>
    """
    return html_content


@app.post("/register", response_model=UserRead)
async def register(request: Request, session: Session = Depends(get_session)):
    form_data = await request.form()
    user_data = UserCreate(
        username=form_data.get("username"),
        email=form_data.get("email"),
        password=form_data.get("password")
    )
    db_user = create_user(session, user_data)
    return db_user


@app.post("/login", response_model=Token)
async def login(request: Request, session: Session = Depends(get_session)):
    form_data = await request.form()
    form = OAuth2PasswordRequestForm(
        username=form_data.get("username"),
        password=form_data.get("password")
    )
    user = authenticate_user(session, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/users", response_class=HTMLResponse)
def get_users(session: Session = Depends(get_session)):
    users = get_all_users(session)
    html_content = """
    <html>
        <body>
            <h1>User List</h1>
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                </tr>
    """
    for user in users:
        html_content += f"""
                <tr>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                </tr>
        """
    html_content += """
            </table>
        </body>
    </html>
    """
    return html_content


@app.post("/incomes", response_model=IncomeRead)
def create_income_endpoint(income: IncomeCreate, current_user: User = Depends(get_current_user),
                           session: Session = Depends(get_session)):
    db_income = create_income(session, income, current_user.id)
    return db_income


@app.get("/incomes", response_model=list[IncomeRead])
def get_incomes_endpoint(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_incomes(session, current_user.id)


@app.post("/expenses", response_model=ExpenseRead)
def create_expense_endpoint(expense: ExpenseCreate, current_user: User = Depends(get_current_user),
                            session: Session = Depends(get_session)):
    db_expense = create_expense(session, expense, current_user.id)
    return db_expense


@app.get("/expenses", response_model=list[ExpenseRead])
def get_expenses_endpoint(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return get_expenses(session, current_user.id)