from flask import Blueprint, render_template, g, redirect, url_for, request, flash
import src.repositories.articles_repository as articles_repository
import src.repositories.categories_repository as categories_repository

articles_bp = Blueprint('articles', __name__)

@articles_bp.route("/articles", methods=["GET"])
def index():
    articles = articles_repository.get_all_articles(g.session)
    return render_template('pages/articles/index.html', articles=articles)

@articles_bp.route("/articles", methods=["POST"])
def search():
    article_name = request.form["article_name"]
    if article_name:
        articles = articles_repository.get_all_articles_by_name(g.session, article_name)
    else: 
        articles = articles_repository.get_all_articles(g.session)
    return render_template('pages/articles/index.html', articles=articles)

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
        categories_id = request.form.getlist("categories_id")
        if categories_id:
            categories = [categories_repository.get_category_by_id(g.session, int(category_id)) for category_id in categories_id]
            article = articles_repository.create_article(g.session, name, price, stock_quantity, categories)
            success = f"article {article.name} was successfully created"
            flash(success, "success")
            return redirect(url_for('articles.index'))
        else:
            error = "Select at least one category"
    if error: flash(error, "error")
    if message: flash(message, "message")
    categories = categories_repository.get_all_categories(g.session)
    return render_template('pages/articles/new.html', categories=categories)

@articles_bp.route("/articles/<int:article_id>/edit")
def edit(article_id: int):
    article = articles_repository.get_article_by_id(g.session, article_id)
    if article is None:
        return render_template('pages/errors/404.html'), 404
    categories = categories_repository.get_all_categories(g.session)
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
    categories_id = request.form.getlist("categories_id")
    if categories_id:
        categories = [categories_repository.get_category_by_id(g.session, int(category_id)) for category_id in categories_id]
        if articles_repository.update_article(g.session, article, name, price, stock_quantity, categories):
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