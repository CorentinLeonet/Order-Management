from flask import Blueprint, render_template, g, redirect, url_for, request
import src.repositories.orders_repository as orders_repository

orders_bp = Blueprint('orders', __name__)

@orders_bp.route("/orders")
def index():
    orders = orders_repository.get_all_orders(g.session)
    return render_template('pages/orders/index.html', orders=orders)

@orders_bp.route("/orders/<int:order_id>")
def show(order_id: int):
    order = orders_repository.get_order_by_id(g.session, order_id)
    if order is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/orders/show.html', order_id=order)

@orders_bp.route("/orders/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        client_id = request.form["client_id"]
        date = request.form["date"]
        status = request.form["status"]
        orders_repository.create_order(g.session, client_id, date, status)
        return redirect(url_for('orders.index'))
    return render_template('pages/orders/new.html')

@orders_bp.route("/orders/<int:order_id>/edit")
def edit(order_id: int):
    order = orders_repository.get_order_by_id(g.session, order_id)
    if order is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/orders/edit.html', order=order)

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