from flask import Blueprint, render_template, g
import src.repositories.orders_repository as orders_repository
import src.repositories.articles_repository as articles_repository
import src.repositories.clients_repository as clients_repository
import src.repositories.categories_repository as categories_repository

stats_bp = Blueprint('stats', __name__)

@stats_bp.route("/stats/orders")
def orders():
    stats_day = orders_repository.get_orders_by_day(g.session)
    stats_month = orders_repository.get_orders_by_month(g.session)
    stats_year = orders_repository.get_orders_by_year(g.session)
    return render_template("pages/stats/nbr_order.html", stats_day=stats_day, stats_month=stats_month, stats_year=stats_year)