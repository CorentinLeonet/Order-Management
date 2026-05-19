from tests.database.database import engine
from src.database.database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from src.Models import *
from src.repositories import categories_repository as categories_repository

if not database_exists(engine.url): create_database(engine.url)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

sessionlocal = sessionmaker(bind=engine)

session = sessionlocal()

category_name = "category_test"
category_description = "Test description"

category_new_name = "category_test_new"
category_new_description = "Test new description"

def test_create_category():
    category = categories_repository.create_category(session, category_name, category_description )
    assert category.name == category_name
    assert category.description == category_description

def test_read_category():
    category = categories_repository.get_category_by_name(session, category_name)
    assert category.name == category_name
    assert category.description == category_description

def test_update_category():
    category = categories_repository.get_category_by_name(session, category_name)
    assert categories_repository.update_category(session, category, category_new_name, category_new_description) == True
    assert category.name == category_new_name
    assert category.description == category_new_description

def test_delete_category():
    category = categories_repository.get_category_by_name(session, category_name)
    categories_repository.delete_category(session, category)
    category = categories_repository.get_category_by_name(session, category_name)
    assert category is None
