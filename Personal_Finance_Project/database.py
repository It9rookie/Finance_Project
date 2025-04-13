from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = "mysql+pymysql://root:wzn001021@localhost:3306/personal_finance"  # 请根据实际情况修改
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)