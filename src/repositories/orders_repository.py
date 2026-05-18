from sqlalchemy.orm import Session
from sqlalchemy import select
from src.Models.Order import Order, Order_Status_Enum
from datetime import datetime
from src.Models.Article import Article
from src.Models.Order_Line import Order_Line


def create_order(session: Session, client_id: int, date: datetime, status=Order_Status_Enum.PENDING.value) -> Order:
    try:
        order = Order(client_id=client_id, date=date, status=status)
        session.add(order)
        session.commit()
        session.refresh(order)
        return order
    except Exception as e:
        session.rollback()
        print(e)
    
def get_order_by_id(session: Session, id: int) -> Order:
    try:
        stmt = select(Order).where(Order.id == id)
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        session.rollback()
        print(e)

def get_all_orders(session: Session) -> list[Order]:
    try:
        stmt = select(Order)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        session.rollback()
        print(e)


def update_order_add_line(session: Session, order: Order, article: Article, quantity: int):
    try:
        order_line = Order_Line(order_id=order.id, article_id=article.id, quantity=quantity, unit_price=article.price)
        article.stock_quantity -= quantity
        session.add(order_line)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)   

def update_order_remove_line(session: Session, order: Order, article: Article) -> bool:
    try:
        stmt = select(Order_Line).where(Order_Line.article_id == article.id, Order_Line == order.id)
        order_line = session.execute(stmt)
        if order_line is None:
            return False
        article.stock_quantity += order_line.quantity
        session.delete(order_line)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(e)   

def delete_order(session: Session, order: Order) -> None:
    try:
        session.delete(order)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

def delete_order_by_id(session: Session, id: int) -> bool:
    try:
        stmt = select(Order).where(Order.id == id)
        order = session.execute(stmt).scalar_one_or_none()

        if order is None:
            return False
        session.delete(order)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(e)