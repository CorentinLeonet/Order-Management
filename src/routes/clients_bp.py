from flask import Blueprint, render_template, g, redirect, url_for, request
import src.repositories.clients_repository as clients_repository
from datetime import datetime

clients_bp = Blueprint('clients', __name__)

@clients_bp.route("/clients")
def index():
    clients = clients_repository.get_all_clients(g.session)
    return render_template('pages/clients/index.html', clients=clients)

@clients_bp.route("/clients/<int:client_id>")
def show(client_id: int):
    client = clients_repository.get_client_by_id(g.session, client_id)
    if client is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/clients/show.html', client=client)

@clients_bp.route("/client/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        firstname = request.form["firstname"]
        surname = request.form["surname"]
        email = request.form["email"]
        date_of_creation = datetime.now()
        clients_repository.create_client(g.session, firstname, surname, email, date_of_creation)
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
    client = clients_repository.get_client_by_id(g.session, client_id)
    if client is None:
        return render_template('pages/errors/404.html'), 404
    name = request.form["name"]
    firstname = request.form["firstname"]
    surname = request.form["surname"]
    email = request.form["email"]
    date_of_creation = request.form["date_of_creation"]
    clients_repository.update_client(g.session, client, firstname, surname, email, date_of_creation)
    return redirect(url_for('clients.index'))

@clients_bp.route("/clients/<int:client_id>/delete", methods=["POST"])
def delete(client_id: int):
    if not clients_repository.delete_client_by_id(g.session, client_id):
        return render_template('pages/errors/404.html'), 404
    return redirect(url_for('clients.index'))