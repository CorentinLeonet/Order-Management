from src.database.database import Base, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from flask import Flask, g, render_template
from src.Models import *
from src.routes.categories_bp import categories_bp
from src.routes.main_bp import main_bp
from src.routes.articles_bp import articles_bp
from src.routes.orders_bp import orders_bp
from src.routes.clients_bp import clients_bp
from src.routes.stats_bp import stats_bp

if not database_exists(engine.url): create_database(engine.url)
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

app = Flask(__name__)
sessionlocal = sessionmaker(bind=engine)

@app.before_request #Open session
def open_session():
    g.session = sessionlocal() 

@app.teardown_request
def close_session(exc):
    session = g.pop('session', None)
    if session:
        if exc is not None:
            session.rollback() #rollback if any exception
        session.close()

@app.errorhandler(500)
def server_error(e):
    return render_template('pages/errors/500.html', error=e), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('pages/errors/404.html', error=e), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template('pages/errors/400.html', error=e), 400
    
app.register_blueprint(categories_bp)
app.register_blueprint(main_bp)
app.register_blueprint(articles_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(clients_bp)
app.register_blueprint(stats_bp)

    
    
