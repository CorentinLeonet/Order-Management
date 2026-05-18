from flask import Blueprint, render_template, g, redirect, url_for, request
import src.repositories.categories_repository as categories_repository

categories_bp = Blueprint('categories', __name__)

@categories_bp.route("/categories")
def index():
    categories = categories_repository.get_all_categories(g.session)
    return render_template('pages/categories/index.html', categories=categories)

@categories_bp.route("/categories/<int:category_id>")
def show(category_id: int):
    category = categories_repository.get_category_by_id(g.session, category_id)
    if category is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/categories/show.html', category=category)

@categories_bp.route("/categories/new", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        categories_repository.create_category(g.session, name, description)
        return redirect(url_for('categories.index'))
    return render_template('pages/categories/new.html')

@categories_bp.route("/categories/<int:category_id>/edit")
def edit(category_id: int):
    category = categories_repository.get_category_by_id(g.session, category_id)
    if category is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/categories/edit.html', category=category)

@categories_bp.route("/categories/<int:category_id>/update", methods=["POST"])
def update(category_id: int):
    category = categories_repository.get_category_by_id(g.session, category_id)
    if category is None:
        return render_template('pages/errors/404.html'), 404
    name = request.form["name"]
    description = request.form["description"]
    categories_repository.update_category(g.session, category, name, description)
    return redirect(url_for('categories.index'))

@categories_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
def delete(category_id: int):
    if not categories_repository.delete_category_by_id(g.session, category_id):
        return render_template('pages/errors/404.html'), 404
    return redirect(url_for('categories.index'))