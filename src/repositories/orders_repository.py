from sqlalchemy.orm import Session
from sqlalchemy import select, func
from src.Models.Order import Order, Order_Status_Enum
from datetime import datetime
from src.Models.Article import Article
from src.Models.Order_Line import Order_Line


def create_order(session: Session, client_id: int, date_ordered: datetime, status=Order_Status_Enum.PENDING.value) -> Order:
    try:
        order = Order(client_id=client_id, date_ordered=date_ordered, status=status)
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
        print(e)

def get_all_orders(session: Session) -> list[Order]:
    try:
        stmt = select(Order)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_total_price(session: Session, order: Order):
    try:
        stmt = select(func.sum(Order_Line.unit_price)).where(Order_Line.order_id == order.id)
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def update_order(session: Session, order: Order, client_id : int, date_ordered : datetime, status: str, date_shipped: datetime, date_recieved : datetime) :
    try:
        order.client_id = client_id
        order.date_ordered = date_ordered
        order.date_shipped = date_shipped
        order.date_recieved = date_recieved
        order.status = status
        session.commit()
    except Exception as e:
        print(e)
        return False

def update_order_add_line(session: Session, order: Order, article: Article, quantity: int):
    try:
        order_line = Order_Line(order_id=order.id, article_id=article.id, quantity=quantity, unit_price=article.price)
        article.stock_quantity -= quantity
        session.add(order_line)
        session.commit()
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

def get_line_by_id(session: Session, id: int) -> Order_Line:
    stmt = select(Order_Line).where(Order_Line.id == id)
    return session.execute(stmt).scalar_one_or_none()

def remove_line(session: Session, line: Order_Line) -> None:
    # stock is restored by the before_delete event on Order_Line
    session.delete(line)
    session.commit()