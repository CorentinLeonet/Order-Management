from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase
import os
from sqlalchemy import create_engine

load_dotenv(dotenv_path="tests/.env.test")

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass