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

def get_count_orders(session: Session) -> int:
    try:
        stmt = select(func.count(Order.id))
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)

def get_total_price(session: Session, order: Order):
    try:
        stmt = select(func.sum(Order_Line.unit_price * Order_Line.quantity)).where(Order_Line.order_id == order.id)
        return session.execute(stmt).scalar_one_or_none()
    except Exception as e:
        print(e)


def get_shipped_orders(session: Session):
    try:
        stmt = select(Order).where(Order.status == Order_Status_Enum.SHIPPED.value)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_cancelled_orders(session: Session):
    try:
        stmt = select(Order).where(Order.status == Order_Status_Enum.CANCELLED.value)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_pending_orders(session: Session):
    try:
        stmt = select(Order).where(Order.status == Order_Status_Enum.PENDING.value)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_confirmed_orders(session: Session):
    try:
        stmt = select(Order).where(Order.status == Order_Status_Enum.CONFIRMED.value)
        return session.execute(stmt).scalars().all()
    except Exception as e:
        print(e)

def get_orders_grouped_by_status(session: Session):
    try:
        stmt = select(Order.status, func.count(Order.id)).group_by(Order.status)
        return session.execute(stmt).fetchall()
    except Exception as e:
        print(e)

def update_order(session: Session, order: Order, client_id : int, date_ordered : datetime, status: str, date_shipped: datetime, date_confirmed : datetime) :
    try:
        if status == Order_Status_Enum.CANCELLED.value and order.status != Order_Status_Enum.CANCELLED.value: #check if status is cancelled and readd the stokc of article automaticaly but only if the previous status was cancelled already
            for line in order.order_lines: 
                line.article.stock_quantity += line.quantity
        order.client_id = client_id
        order.date_ordered = date_ordered
        order.date_shipped = date_shipped
        order.date_confirmed = date_confirmed
        order.status = status
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def update_order_add_line(session: Session, order: Order, article: Article, quantity: int):
    try:
        stmt = select(Order_Line).where(
            Order_Line.order_id == order.id,
            Order_Line.article_id == article.id
        ) 
        existing_order_line = session.execute(stmt).scalar_one_or_none()
        if existing_order_line: # check if a line for this article already exists and modify article stock and line accordingly
            article.stock_quantity -= quantity
            existing_order_line.quantity += quantity
        else: # if not add a line
            order_line = Order_Line(order_id=order.id, article_id=article.id, quantity=quantity, unit_price=article.price)
            article.stock_quantity -= quantity
            session.add(order_line)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

def update_order_update_order_line_quantity(session: Session, order_line: Order_Line, quantity: int):
    try:
        difference = order_line.quantity - quantity
        order_line.article.stock_quantity += difference
        order_line.quantity = quantity
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

def delete_order(session: Session, order: Order):
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
        for order_Line in order.order_lines: #refill the article stock
            order_Line.article.stock_quantity += order_Line.quantity
            session.delete(order_Line)
        session.delete(order)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(e)

def get_line_by_id(session: Session, id: int) -> Order_Line:
    stmt = select(Order_Line).where(Order_Line.id == id)
    return session.execute(stmt).scalar_one_or_none()

def remove_line(session: Session, order_line: Order_Line) -> None:
    order_line.article.stock_quantity += order_line.quantity
    session.delete(order_line)
    session.commit()