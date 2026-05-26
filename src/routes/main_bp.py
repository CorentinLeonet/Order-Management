from flask import Blueprint, render_template, g
import src.repositories.orders_repository as orders_repository
import src.repositories.articles_repository as articles_repository
import src.repositories.clients_repository as clients_repository
import src.repositories.categories_repository as categories_repository
import src.repositories.stats_repository as stats_repository

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():

    order_count = orders_repository.get_count_orders(g.session)
    article_count = articles_repository.get_count_articles(g.session)
    client_count = clients_repository.get_count_clients(g.session)
    category_count = categories_repository.get_count_categories(g.session)

    order_pie_chart_rows = stats_repository.get_orders_grouped_by_status(g.session)
    article_pie_chart_rows = stats_repository.get_articles_count_sales(g.session)
    client_pie_chart_rows = stats_repository.get_clients_count_orders(g.session)
    category_pie_chart_rows = stats_repository.get_categories_count_articles(g.session)

    return render_template('pages/index.html',
                            order_count=order_count,
                            article_count=article_count,
                            client_count=client_count,
                            category_count=category_count,
        
                            order_pie_chart_rows=order_pie_chart_rows,
                            article_pie_chart_rows=article_pie_chart_rows,
                            client_pie_chart_rows=client_pie_chart_rows,
                            category_pie_chart_rows=category_pie_chart_rows
    )