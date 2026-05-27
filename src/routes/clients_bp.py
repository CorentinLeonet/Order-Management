from flask import Blueprint, render_template, g, redirect, url_for, request, flash
import src.repositories.clients_repository as clients_repository
from datetime import datetime

clients_bp = Blueprint('clients', __name__)

@clients_bp.route("/clients", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search = request.args.get("client_name")

    if search:
        clients, total = clients_repository.get_clients_paginated(
            g.session, page, per_page, search
        )
    else:
        clients, total = clients_repository.get_clients_paginated(
            g.session, page, per_page
        )

    has_next = page * per_page < total
    has_prev = page > 1
    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "pages/clients/index.html",
        clients=clients,
        page=page,
        has_next=has_next,
        has_prev=has_prev,
        total_pages=total_pages,
        search=search
    )

@clients_bp.route("/clients/<int:client_id>")
def show(client_id: int):
    client = clients_repository.get_client_by_id(g.session, client_id)
    if client is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/clients/show.html', client=client)

@clients_bp.route("/client/new", methods=["GET", "POST"])
def create():
    error = None
    success = None
    if request.method == "POST":
        firstname = request.form["firstname"]
        surname = request.form["surname"]
        email = request.form["email"]
        date_of_creation = datetime.now()
        client = clients_repository.create_client(g.session, firstname, surname, email, date_of_creation)
        if client:
            success = f"client {firstname} {surname} was successfully created"
        else:
            error = f"client {firstname} {surname} could not be created"
        if error: flash(error, "error")
        if success: flash(success, "success")
        return redirect(url_for('clients.index'))
    return render_template('pages/clients/new.html')

@clients_bp.route("/clients/<int:client_id>/edit")
def edit(client_id: int):
    client = clients_repository.get_client_by_id(g.session, client_id)
    if client is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/clients/edit.html', client=client)

@clients_bp.route("/clients/<int:client_id>/update", methods=["POST"])
def update(client_id: int):
    error = None
    success = None
    client = clients_repository.get_client_by_id(g.session, client_id)
    if client is None:
        return render_template('pages/errors/404.html'), 404
    firstname = request.form["firstname"]
    surname = request.form["surname"]
    email = request.form["email"]
    date_of_creation = request.form["date_of_creation"]
    if request.form.get("active"):
        active = True
    else:
        active = False
    if clients_repository.update_client(g.session, client, firstname, surname, email, date_of_creation, active):
        success = f"client {firstname} {surname} was successfully updated"
    else:
        error = f"client {firstname} {surname} could not be updated"
    if error: flash(error, "error")
    if success: flash(success, "success")
    return redirect(url_for('clients.show', client_id=client_id))

@clients_bp.route("/clients/<int:client_id>/delete", methods=["POST"])
def delete(client_id: int):
    error = None
    success = None
    if clients_repository.delete_client_by_id(g.session, client_id):
        success = f"client was successfully deleted"
    else:
        error = f"client could not be deleted"
    if error: flash(error, "error")
    if success: flash(success, "success")
    return redirect(url_for('clients.index'))