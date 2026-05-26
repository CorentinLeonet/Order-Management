from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.Models.Article import Article
from src.Models.Order_Line import Order_Line


def create_article(session: Session, name: str, price: int, stock_quantity: int, categories: list) -> Article:
    try:
        article = Article(name=name, price=price, stock_quantity=stock_quantity, categories=categories)
        session.add(article)
        session.commit()
        session.refresh(article)
        return article
    except Exception as e:
        print(e)
    
def get_article_by_id(session: Session, id: int) -> Article:
    try:
        stmt = select(Article).where(Article.id == id)
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_all_articles(session: Session) -> list[Article]:
    try:
        stmt = select(Article)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_count_articles(session: Session) -> int:
    try: 
        stmt = select(func.count(Article.id))
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_articles_count_sales(session: Session):
    try: 
        stmt = select(Article.name, func.sum(Order_Line.quantity)).join(Order_Line, onclause=Order_Line.article_id == Article.id).group_by(Article.name)
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)
        
def get_all_articles_by_name(session: Session, article_name: str):
    try:
        stmt = select(Article).where(Article.name.ilike("%" + article_name + "%"))
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def delete_article(session: Session, article: Article) -> None:
    try:
        session.delete(article)
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def update_article(session: Session, article: Article, name: str, price: int, stock_quantity: int, categories: list):
    try:
        article.name = name
        article.price = price
        article.stock_quantity = stock_quantity
        article.categories = categories
        session.commit()
    except Exception  as e:
        print(e)
        return False
    return True

def delete_article_by_id(session: Session, id: int) -> bool:
    try:
        stmt = select(Article).where(Article.id == id)
        article = session.execute(stmt).scalar_one_or_none()

        if article is None:
            return False
        session.delete(article)
        session.commit()
    except Exception as e:
        print(e)
        return False
    return True