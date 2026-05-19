from src.repositories import articles_repository as articles_repository
from src.repositories import categories_repository as categories_repository
from tests.conftest import ARTICLE_NAME, ARTICLE_PRICE, ARTICLE_STOCK


category_name = "category_article_test"
category_description = "Test description"




article_new_name = "article__new_test"
article_new_price = 100
article_new_stock_quantity = 1000

def test_create_article(session, article):
    assert article.name == ARTICLE_NAME
    assert article.price == ARTICLE_PRICE
    assert article.stock_quantity == ARTICLE_STOCK

def test_read_article(session, article):
    fetched_article = articles_repository.get_article_by_id(session, article.id)
    assert fetched_article is not None
    assert fetched_article.id == article.id
    assert fetched_article.name == ARTICLE_NAME

def test_update_article(session, article):
    assert articles_repository.update_article(session, article, article_new_name, article_new_price, article_new_stock_quantity, article.categories) == True
    assert article.name == article_new_name
    assert article.price == article_new_price
    assert article.stock_quantity == article_new_stock_quantity

def test_delete_article(session, article):
    articles_repository.delete_article(session, article)
    assert articles_repository.get_article_by_id(session, article.id) is None