from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.Models.Client import Client
from src.Models.Category import Category
from src.Models.Article_Category import Article_Category
from src.Models.Article import Article
from src.Models.Order_Line import Order_Line
from src.Models.Order import Order, Order_Status_Enum
from datetime import datetime


def get_articles_by_day(session: Session):
    try: 
        day = func.DATE_TRUNC("day", Order.date_ordered)
        today = func.DATE_TRUNC("day", datetime.today())
        stmt = select(
            Article.name, func.sum(Order_Line.quantity)
            ).join(
                Order_Line, onclause=Order_Line.article_id == Article.id
            ).join(
                Order, onclause=Order_Line.order_id == Order.id
            ).where(
                day == today, Order.status != Order_Status_Enum.CANCELLED.value
            ).group_by(
                day, Article.name
            )
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)

def get_articles_by_month(session: Session):
    try: 
        month = func.DATE_TRUNC("month", Order.date_ordered)
        this_month = func.DATE_TRUNC("month", datetime.today())
        stmt = select(
            Article.name, func.sum(Order_Line.quantity)
            ).join(
                Order_Line, onclause=Order_Line.article_id == Article.id
            ).join(
                Order, onclause=Order_Line.order_id == Order.id
            ).where(
                month == this_month, Order.status != Order_Status_Enum.CANCELLED.value
            ).group_by(
                month, Article.name
            )
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)

def get_articles_by_year(session: Session):
    try: 
        year = func.DATE_TRUNC("year", Order.date_ordered)
        this_year = func.DATE_TRUNC("year", datetime.today())
        stmt = select(
            Article.name, func.sum(Order_Line.quantity)
            ).join(
                Order_Line, onclause=Order_Line.article_id == Article.id
            ).join(
                Order, onclause=Order_Line.order_id == Order.id
            ).where(
                year == this_year, Order.status != Order_Status_Enum.CANCELLED.value
            ).group_by(
                year, Article.name
            )
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)

def get_orders_by_day(session: Session):
    day = func.DATE_TRUNC("day", Order.date_ordered)
    stmt = select(day, func.count(Order.id)).group_by(day)
    return session.execute(stmt).fetchall()

def get_orders_by_month(session: Session):
    month = func.DATE_TRUNC("month", Order.date_ordered)
    stmt = select(month, func.count(Order.id)).group_by(month)
    return session.execute(stmt).fetchall()

def get_orders_by_year(session: Session):
    year = func.DATE_TRUNC("year", Order.date_ordered)
    stmt = select(year, func.count(Order.id)).group_by(year)
    return session.execute(stmt).fetchall()

def get_articles_count_sales(session: Session):
    try: 
        stmt = select(
            Article.name, func.sum(Order_Line.quantity)
            ).join(
                Order_Line, onclause=Order_Line.article_id == Article.id
            ).where(
                Order.status != Order_Status_Enum.CANCELLED.value
            ).group_by(
                Article.name
            )
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)

def get_clients_count_orders(session: Session):
    try: 
        stmt = select(
            func.concat(Client.firstname, Client.surname), func.count(Order.id)
            ).where(
                Order.client_id == Client.id, Order.status != Order_Status_Enum.CANCELLED.value
            ).group_by(
                func.concat(Client.firstname, Client.surname), Client.id
            )
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)

def get_categories_count_articles(session: Session):
    try: 
        stmt = select(
            Category.name, func.count(Article_Category.article_id)
            ).where(
                Article_Category.category_id == Category.id
            ).group_by(
                Category.name
            )
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)

def get_orders_grouped_by_status(session: Session):
    try:
        stmt = select(
            Order.status, func.count(Order.id)
            ).group_by(
                Order.status
            )
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)