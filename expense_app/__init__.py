from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "project.sqlite3"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abulaman'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .models import Entry

    create_db(app)
    
    return app


def create_db(app):
    if not path.exists("expense_app/"+ DB_NAME):
        db.create_all(app=app)
    else:
        print('DATABASE ALREADY EXISTS')