from flask import Blueprint, render_template, g, redirect, url_for, request, flash
import src.repositories.categories_repository as categories_repository

categories_bp = Blueprint('categories', __name__)

@categories_bp.route("/categories", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search = request.args.get("category_name")

    if search:
        categories, total = categories_repository.get_categories_paginated(
            g.session, page, per_page, search
        )
    else:
        categories, total = categories_repository.get_categories_paginated(
            g.session, page, per_page
        )

    has_next = page * per_page < total
    has_prev = page > 1
    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "pages/categories/index.html",
        categories=categories,
        page=page,
        has_next=has_next,
        has_prev=has_prev,
        total_pages=total_pages,
        search=search
    )

@categories_bp.route("/categories/<int:category_id>")
def show(category_id: int):
    category = categories_repository.get_category_by_id(g.session, category_id)
    if category is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/categories/show.html', category=category)

@categories_bp.route("/categories/new", methods=["GET", "POST"])
def create():
    error = None
    success = None
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        category = categories_repository.create_category(g.session, name, description)
        if category:
            success = f"category {name} was successfully created"
        else:
            error = f"could not create category {name}"
        if error: flash(error, "error")
        if success: flash(success, "success")
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
    error = None
    success = None
    category = categories_repository.get_category_by_id(g.session, category_id)
    if category is None:
        return render_template('pages/errors/404.html'), 404
    name = request.form["name"]
    description = request.form["description"]
    if request.form.get("active"):
        active = True
    else:
        active = False
    if categories_repository.update_category(g.session, category, name, description, active):
        success = f"category {name} was successfully updated"
    else:
        error = f"could not update category {name}"
    if error: flash(error, "error")
    if success: flash(success, "success")
    return redirect(url_for('categories.show', category_id=category_id))

@categories_bp.route("/categories/<int:category_id>/delete", methods=["POST"])
def delete(category_id: int):
    error = None
    success = None
    if categories_repository.delete_category_by_id(g.session, category_id):
        success = f"category was successfully deleted"
    else:
        error = f"could not delete category"
    if error: flash(error, "error")
    if success: flash(success, "success")
    return redirect(url_for('categories.index'))