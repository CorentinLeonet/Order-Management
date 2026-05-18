from flask import Blueprint, render_template, g, redirect, url_for, request
import src.repositories.articles_repository as articles_repository

articles_bp = Blueprint('articles', __name__)

@articles_bp.route("/articles")
def index():
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
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        stock_quantity = request.form["stock_quantity"]
        categories = request.form["categories"]
        articles_repository.create_article(g.session, name, price, stock_quantity, categories)
        return redirect(url_for('articles.index'))
    return render_template('pages/articles/new.html')

@articles_bp.route("/articles/<int:article_id>/edit")
def edit(article_id: int):
    article = articles_repository.get_article_by_id(g.session, article_id)
    if article is None:
        return render_template('pages/errors/404.html'), 404
    return render_template('pages/articles/edit.html', article=article)

@articles_bp.route("/articles/<int:article_id>/update", methods=["POST"])
def update(article_id: int):
    article = articles_repository.get_article_by_id(g.session, article_id)
    if article is None:
        return render_template('pages/errors/404.html'), 404
    name = request.form["name"]
    price = request.form["price"]
    stock_quantity = request.form["stock_quantity"]
    categories = request.form["categories"]
    articles_repository.update_article(g.session, article, name, price, stock_quantity, categories)
    return redirect(url_for('articless.index'))

@articles_bp.route("/articles/<int:article_id>/delete", methods=["POST"])
def delete(article_id: int):
    if not articles_repository.delete_article_by_id(g.session, article_id):
        return render_template('pages/errors/404.html'), 404
    return redirect(url_for('articles.index'))