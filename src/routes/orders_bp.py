from flask import Blueprint, render_template, g, redirect, url_for, request, send_file
import io
import src.repositories.orders_repository as orders_repository
import src.repositories.clients_repository as clients_repository
import src.repositories.articles_repository as articles_repository
from src.Models.Order import Order_Status_Enum
from datetime import datetime
from fpdf import FPDF

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
    total_price = orders_repository.get_total_price(g.session, order)
    if total_price is None:
        total_price = 0
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

@orders_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
def delete(order_id: int):
    if not orders_repository.delete_order_by_id(g.session, order_id):
        return render_template('pages/errors/404.html'), 404
    return redirect(url_for('orders.index'))


@orders_bp.route("/orders/<int:order_id>/edit")
def edit(order_id: int):
    order = orders_repository.get_order_by_id(g.session, order_id)
    if order is None:
        return render_template('pages/errors/404.html'), 404
    articles = articles_repository.get_all_articles(g.session)
    match order.status:
        case Order_Status_Enum.PENDING.value:
            all_status = [Order_Status_Enum.PENDING.value, Order_Status_Enum.CONFIRMED.value, Order_Status_Enum.CANCELLED.value]
        case Order_Status_Enum.CONFIRMED.value:
            all_status = [Order_Status_Enum.CONFIRMED.value, Order_Status_Enum.SHIPPED.value, Order_Status_Enum.CANCELLED.value]
        case Order_Status_Enum.SHIPPED.value:
            all_status = [Order_Status_Enum.SHIPPED.value, Order_Status_Enum.CANCELLED.value]
        case Order_Status_Enum.CANCELLED.value:
            all_status = [Order_Status_Enum.CANCELLED.value]
    return render_template('pages/orders/edit.html',
        order=order,
        articles=articles,
        all_status=all_status
    )

@orders_bp.route("/orders/<int:order_id>/update", methods=["POST"])
def update(order_id: int):
    order = orders_repository.get_order_by_id(g.session, order_id)
    if order is None:
        return render_template('pages/errors/404.html'), 404
    status = request.form["status"]
    date_confirmed = order.date_confirmed
    date_shipped = order.date_shipped
    if order.date_shipped is None:
        date_shipped = request.form.get("date_shipped") or None
        if date_shipped:
            date_shipped = datetime.fromisoformat(date_shipped)
    if order.date_confirmed is None:
        date_confirmed = request.form.get("date_confirmed") or None
        if date_confirmed:
            date_confirmed = datetime.fromisoformat(date_confirmed)
    if status != order.status:
        if status == Order_Status_Enum.CONFIRMED.value:
            date_confirmed = datetime.now()
        elif status == Order_Status_Enum.SHIPPED.value:
            date_shipped = datetime.now()
   
    orders_repository.update_order(g.session, order,
        order.client_id, order.date_ordered,
        status, date_shipped, date_confirmed
    )
    return redirect(url_for('orders.edit', order_id=order_id))

@orders_bp.route("/orders/<int:order_id>/order_lines/add", methods=["POST"])
def add_line(order_id: int):
    order = orders_repository.get_order_by_id(g.session, order_id)
    if order is None:
        return render_template('pages/errors/404.html'), 404
    article_id = int(request.form["article_id"])
    quantity = int(request.form["quantity"])
    article = articles_repository.get_article_by_id(g.session, article_id)
    if article is None or article.stock_quantity < quantity:
        return redirect(url_for('orders.edit', order_id=order_id))
    orders_repository.update_order_add_line(g.session, order, article, quantity)
    return redirect(url_for('orders.edit', order_id=order_id))

@orders_bp.route("/orders/<int:order_id>/lines/<int:order_line_id>/update", methods=["POST"])
def update_line(order_id: int, order_line_id: int):
    order_line = orders_repository.get_line_by_id(g.session, order_line_id)
    if order_line is None:
        return render_template('pages/errors/404.html'), 404
    quantity = int(request.form["quantity"])
    orders_repository.update_order_update_order_line_quantity(g.session, order_line, quantity)
    return redirect(url_for('orders.edit', order_id=order_id))

@orders_bp.route("/orders/<int:order_id>/order_lines/<int:order_line_id>/delete", methods=["POST"])
def delete_line(order_id: int, order_line_id: int):
    line = orders_repository.get_line_by_id(g.session, order_line_id)
    if line is None:
        return render_template('pages/errors/404.html'), 404
    orders_repository.remove_line(g.session, line)
    return redirect(url_for('orders.edit', order_id=order_id))

@orders_bp.route("/orders/<int:order_id>/bill")
def bill(order_id: int):
    order = orders_repository.get_order_by_id(g.session, order_id)
    if order is None:
        return render_template('pages/errors/404.html'), 404

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Bill - Order #{order.id}", ln=True)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Client: {order.client.firstname} {order.client.surname}", ln=True)
    pdf.cell(0, 8, f"Date: {order.date_ordered.strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 8, f"Status: {order.status}", ln=True)
    pdf.ln(5)

    # table header
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(80, 8, "Article", border=1)
    pdf.cell(30, 8, "Unit price", border=1)
    pdf.cell(30, 8, "Quantity", border=1)
    pdf.cell(40, 8, "Total", border=1, ln=True)

    # table rows
    pdf.set_font("Helvetica", "", 11)
    total = 0
    for line in order.order_lines:
        line_total = line.unit_price * line.quantity
        total += line_total
        pdf.cell(80, 8, line.article.name, border=1)
        pdf.cell(30, 8, str(line.unit_price), border=1)
        pdf.cell(30, 8, str(line.quantity), border=1)
        pdf.cell(40, 8, str(line_total), border=1, ln=True)

    # total
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(140, 8, "Total", border=1)
    pdf.cell(40, 8, str(total), border=1, ln=True)

    # send as file download
    pdf_bytes = pdf.output()
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"bill_order_{order.id}.pdf"
    )