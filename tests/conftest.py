import pytest
from tests.database.database import engine
from src.database.database import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from src.Models import *
from src.repositories import articles_repository
from src.repositories import categories_repository
from src.repositories import orders_repository
from src.repositories import clients_repository
from src.Models.Order import Order_Status_Enum
from datetime import datetime

if not database_exists(engine.url): create_database(engine.url)
sessionlocal = sessionmaker(bind=engine)

@pytest.fixture
def session():
    return sessionlocal()

@pytest.fixture(autouse=True) #autouse -> is called on every test
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with sessionlocal() as session:
        yield session

ARTICLE_NAME = "article_test"
ARTICLE_PRICE = 10
ARTICLE_STOCK = 100

CATEGORY_NAME = "cat"
CATEGORY_DESCRIPTION = "desc"

@pytest.fixture
def category(session):
    return categories_repository.create_category(session, CATEGORY_NAME, CATEGORY_DESCRIPTION)

@pytest.fixture
def article(session, category):
    return articles_repository.create_article(session, ARTICLE_NAME, ARTICLE_PRICE, ARTICLE_STOCK, [category])

@pytest.fixture
def client(session):
    return clients_repository.create_client(session, "Bob", "LeBricoleur", "bob@exemple.com", datetime.now())

@pytest.fixture
def order(session, client):
    return orders_repository.create_order(session, client.id, datetime.now())

