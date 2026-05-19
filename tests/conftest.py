import pytest
from tests.database.database import engine
from src.database.database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from src.Models import *

if not database_exists(engine.url): create_database(engine.url)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

sessionlocal = sessionmaker(bind=engine)

@pytest.fixture
def session():
    return sessionlocal()