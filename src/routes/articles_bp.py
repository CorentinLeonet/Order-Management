from flask import Blueprint, render_template, g, redirect, url_for, request, flash
import src.repositories.articles_repository as articles_repository
import src.repositories.categories_repository as categories_repository

articles_bp = Blueprint('articles', __name__)

@articles_bp.route("/articles", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 10
    search = request.args.get("article_name")

    if search:
        articles, total = articles_repository.get_articles_paginated(
            g.session, page, per_page, search
        )
    else:
        articles, total = articles_repository.get_articles_paginated(
            g.session, page, per_page
        )

    has_next = page * per_page < total
    has_prev = page > 1
    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "pages/articles/index.html",
        articles=articles,
        page=page,
        has_next=has_next,
        has_prev=has_prev,
        total_pages=total_pages,
        search=search
    )

@articles_bp.route("/articles/<int:article_id>")
def show(article_id: int):
    article = articles_repository.get_article_by_id(g.session, article_id)
    if article is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/articles/show.html', article=article)

@articles_bp.route("/articles/new", methods=["GET", "POST"])
def create():
    error = None
    message=None
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        price = int(float(price) * 100)
        stock_quantity = request.form["stock_quantity"]
        vat = request.form["vat"]
        categories_id = request.form.getlist("categories_id")
        if categories_id:
            categories = [categories_repository.get_category_by_id(g.session, int(category_id)) for category_id in categories_id]
            article = articles_repository.create_article(g.session, name, price, stock_quantity, categories, vat)
            success = f"article {article.name} was successfully created"
            flash(success, "success")
            return redirect(url_for('articles.index'))
        else:
            error = "Select at least one category"
    if error: flash(error, "error")
    if message: flash(message, "message")
    categories = categories_repository.get_all_active_categories(g.session)
    return render_template('pages/articles/new.html', categories=categories)

@articles_bp.route("/articles/<int:article_id>/edit")
def edit(article_id: int):
    article = articles_repository.get_article_by_id(g.session, article_id)
    if article is None:
        return render_template('pages/errors/404.html'), 404
    categories = categories_repository.get_all_active_categories(g.session)
    return render_template('pages/articles/edit.html', article=article, categories=categories)

@articles_bp.route("/articles/<int:article_id>/update", methods=["POST"], )
def update(article_id: int):
    error = None
    success = None
    article = articles_repository.get_article_by_id(g.session, article_id)
    if article is None:
        return render_template('pages/errors/404.html'), 404
    name = request.form["name"]
    price = request.form["price"]
    price = int(float(price) * 100)
    stock_quantity = request.form["stock_quantity"]
    vat = request.form["vat"]
    if request.form.get("active"):
        active = True
    else:
        active = False
    categories_id = request.form.getlist("categories_id")
    if categories_id:
        categories = [categories_repository.get_category_by_id(g.session, int(category_id)) for category_id in categories_id]
        if articles_repository.update_article(g.session, article, name, price, stock_quantity, categories, vat, active):
            success = f"article {article.name} was successfully updated"
        else:
            error = "error in the form"
    else:
        error = "Select at least one category"
    if error: flash(error, "error")
    if success: flash(success, "success")
    return redirect(url_for('articles.show', article_id=article_id))

@articles_bp.route("/articles/<int:article_id>/delete", methods=["POST"])
def delete(article_id: int):
    error = None
    success = None
    if articles_repository.delete_article_by_id(g.session, article_id):
        success = f"article was successfully deleted"
    else:
        error = f"article could not be deleted"

    if error: flash(error, "error")
    if success: flash(success, "success")
    return redirect(url_for('articles.index'))