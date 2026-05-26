from flask import Blueprint, render_template, g
import src.repositories.stats_repository as stats_repository

stats_bp = Blueprint('stats', __name__)

@stats_bp.route("/stats/orders")
def orders():
    stats_day = stats_repository.get_orders_by_day(g.session)
    stats_month = stats_repository.get_orders_by_month(g.session)
    stats_year = stats_repository.get_orders_by_year(g.session)
    return render_template("pages/stats/stats_orders.html", stats_day=stats_day, stats_month=stats_month, stats_year=stats_year)

@stats_bp.route("/stats/articles")
def articles():
    stats_day = stats_repository.get_articles_by_day(g.session)
    stats_month = stats_repository.get_articles_by_month(g.session)
    stats_year = stats_repository.get_articles_by_year(g.session)
    return render_template("pages/stats/stats_articles.html", stats_day=stats_day, stats_month=stats_month, stats_year=stats_year)
