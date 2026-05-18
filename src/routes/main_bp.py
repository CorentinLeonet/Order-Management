from flask import Blueprint, render_template, g
import src.repositories.orders_repository as orders_repo
import src.repositories.articles_repository as articles_repo
import src.repositories.clients_repository as clients_repo
import src.repositories.categories_repository as categories_repo

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template('pages/index.html', #use sql COUNT for better performance
        order_count=len(orders_repo.get_all_orders(g.session)),
        article_count=len(articles_repo.get_all_articles(g.session)),
        client_count=len(clients_repo.get_all_clients(g.session)),
        category_count=len(categories_repo.get_all_categories(g.session))
    )