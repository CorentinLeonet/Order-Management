from sqlalchemy.orm import Session
from sqlalchemy import select
from src.Models.Article import Article


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

def delete_article(session: Session, article: Article) -> None:
    try:
        session.delete(article)
        session.commit()
    except Exception as e:
        print(e)

def delete_article_by_id(session: Session, id: int) -> bool:
    try:
        stmt = select(Article).where(Article.id == id)
        article = session.execute(stmt).scalar_one_or_none()

        if article is None:
            return False
        session.delete(article)
        session.commit()
        return True
    except Exception as e:
        print(e)