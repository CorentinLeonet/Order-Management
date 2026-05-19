from src.repositories import articles_repository as articles_repository
from src.repositories import categories_repository as categories_repository


category_name = "category_article_test"
category_description = "Test description"



article_name = "article_test"
article_price = 50
article_stock_quantity = 500

article_new_name = "article__new_test"
article_new_price = 100
article_new_stock_quantity = 1000

def test_create_article(session):
    category = categories_repository.create_category(session, category_name, category_description)
    article_categories = [category]
    article = articles_repository.create_article(session, article_name, article_price, article_stock_quantity, article_categories)
    assert article.name == article_name
    assert article.price == article_price
    assert article.stock_quantity == article_stock_quantity
    assert article.categories == article_categories
    
def test_read_article(session):
    article = articles_repository.get_article_by_id(session, 1)
    assert article.name == article_name
    assert article.price == article_price
    assert article.stock_quantity == article_stock_quantity

def test_update_article(session):
    article = articles_repository.get_article_by_id(session, 1)
    assert articles_repository.update_article(session, article, article_new_name, article_new_price, article_new_stock_quantity, article.categories) == True
    assert article.name == article_new_name
    assert article.price == article_new_price
    assert article.stock_quantity == article_new_stock_quantity

def test_delete_article(session):
    article = articles_repository.get_article_by_id(session, 1)
    articles_repository.delete_article(session, article)
    article = articles_repository.get_article_by_id(session, 1)
    assert article is None
