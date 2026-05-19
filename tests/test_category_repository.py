from database.database import Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from src.Models import *
from src.repositories import categories_repository as categories_repository
import pytest

if not database_exists(engine.url): create_database(engine.url)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

sessionlocal = sessionmaker(bind=engine)

session = sessionlocal()

def test_create_category():
    category_name = "category_test"
    category_description = "Test description"
    category = categories_repository.create_category(session, category_name, category_description )
    assert category.name == category_description
    assert category.description == category_description
