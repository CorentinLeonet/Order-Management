from src.repositories import orders_repository
from src.Models.Order import Order_Status_Enum

def test_add_line_reduces_stock(session, order, article):
    orders_repository.update_order_add_line(session, order, article, 10)
    assert article.stock_quantity == 90

def test_remove_line_restores_stock(session, order, article):
    orders_repository.update_order_add_line(session, order, article, 10)
    line = orders_repository.get_line_by_id(session, order.order_lines[0].id)
    orders_repository.remove_line(session, line)
    assert article.stock_quantity == 100

def test_cancel_order_restores_stock(session, order, article):
    orders_repository.update_order_add_line(session, order, article, 10)
    orders_repository.update_order(session, order, order.client_id, order.date_ordered,
        Order_Status_Enum.CANCELLED.value, None, None)
    assert article.stock_quantity == 100

def test_update_line_quantity_adjusts_stock(session, order, article):
    orders_repository.update_order_add_line(session, order, article, 10)
    line = order.order_lines[0]
    orders_repository.update_order_update_order_line_quantity(session, line, 5)
    assert article.stock_quantity == 95