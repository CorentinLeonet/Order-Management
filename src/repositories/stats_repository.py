from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.Models.Article import Article
from src.Models.Order_Line import Order_Line
from src.Models.Order import Order
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
                day == today
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
                month == this_month
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
                year == this_year
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