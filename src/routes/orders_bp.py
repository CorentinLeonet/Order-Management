from flask import Blueprint, render_template, g, redirect, url_for, request
import src.repositories.orders_repository as orders_repository
import src.repositories.clients_repository as clients_repository
from src.Models.Order import Order_Status_Enum
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route("/orders")
def index():
    orders = orders_repository.get_all_orders(g.session)
    return render_template('pages/orders/index.html', orders=orders)

@orders_bp.route("/orders/<int:order_id>")
def show(order_id: int):
    order = orders_repository.get_order_by_id(g.session, order_id)
    total_price = orders_repository.get_total_price(g.session, order)
    if total_price is None:
        total_price = 0
    if order is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/orders/show.html', order=order, total_price=total_price)

@orders_bp.route("/orders/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        client_id = request.form["client_id"]
        date_ordered = datetime.now()
        orders_repository.create_order(g.session, client_id, date_ordered)
        return redirect(url_for('orders.index'))
    clients = clients_repository.get_all_clients(g.session)
    return render_template('pages/orders/new.html', clients=clients)

@orders_bp.route("/orders/<int:order_id>/edit")
def edit(order_id: int):
    order = orders_repository.get_order_by_id(g.session, order_id)
    all_status = Order_Status_Enum._member_map_.values()
    if order is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/orders/edit.html', order=order, all_status=all_status)

@orders_bp.route("/orders/<int:order_id>/update", methods=["POST"])
def update(order_id: int):
    article = orders_repository.get_order_by_id(g.session, order_id)
    if article is None:
        return render_template('pages/errors/404.html'), 404
    client_id = request.form["client_id"]
    date = request.form["date"]
    status = request.form["status"]
    orders_repository.update_order(g.session, client_id, date, status)
    return redirect(url_for('articless.index'))

@orders_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
def delete(order_id: int):
    if not orders_repository.delete_order_by_id(g.session, order_id):
        return render_template('pages/errors/404.html'), 404
    return redirect(url_for('orders.index'))