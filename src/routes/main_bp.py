from flask import Blueprint, render_template, g
import src.repositories.orders_repository as orders_repository
import src.repositories.articles_repository as articles_repository
import src.repositories.clients_repository as clients_repository
import src.repositories.categories_repository as categories_repository

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():

    order_count=orders_repository.get_count_orders(g.session)
    article_count=articles_repository.get_count_articles(g.session)
    client_count=clients_repository.get_count_clients(g.session)
    category_count=categories_repository.get_count_categories(g.session)

    order_pie_chart_rows = orders_repository.get_orders_grouped_by_status(g.session)

    return render_template('pages/index.html', #use sql COUNT for better performance
                            order_count=order_count,
                            article_count=article_count,
                            client_count=client_count,
                            category_count=category_count,
        
                            order_pie_chart_rows=order_pie_chart_rows

    )