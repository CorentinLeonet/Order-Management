from src.repositories import orders_repository as orders_repository
from datetime import datetime
from tests.conftest import ORDER_DATE
from src.Models.Order import Order_Status_Enum


order_new_date = datetime.strptime("21/05/2026", "%d/%m/%Y")
order_new_status = Order_Status_Enum.CONFIRMED.value
order_date_confirmed = datetime.strptime("21/05/2026", "%d/%m/%Y")
order_date_shipped = datetime.strptime("21/05/2026", "%d/%m/%Y")

def test_create_order(session, order, client):
    assert order.client_id == client.id
    assert order.date_ordered == ORDER_DATE
    assert order.date_confirmed == None
    assert order.date_shipped == None

def test_read_order(session, order, client):
    fetched_order = orders_repository.get_order_by_id(session, order.id)
    assert fetched_order.client_id == client.id
    assert fetched_order.date_ordered == ORDER_DATE
    assert fetched_order.date_confirmed == None
    assert fetched_order.date_shipped == None


def test_update_order(session, order, client):
    assert orders_repository.update_order(session, order, client.id, order_new_date, order_new_status, order_date_shipped, order_date_confirmed) == True
    assert order.client_id == client.id
    assert order.status == order_new_status
    assert order.date_ordered == order_new_date
    assert order.date_confirmed == order_date_confirmed
    assert order.date_shipped == order_date_shipped

def test_delete_order(session, order):
    orders_repository.delete_order(session, order)
    assert orders_repository.get_order_by_id(session, order.id) is None