from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.secret_key = 'buitienhoi1510'
    app.config['SECRET_KEY'] = 'buitienhoi15102003'
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hello_bth_user:Zibe1OqHaK8zbdttdXUPvu8ClRSJf0kC@dpg-cqpi1hbqf0us73aj41m0-a.oregon-postgres.render.com/hello_bth"
    #postgresql://hello_bth_user:Zibe1OqHaK8zbdttdXUPvu8ClRSJf0kC@dpg-cqpi1hbqf0us73aj41m0-a.oregon-postgres.render.com/hello_bth
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(views, url_prefic='/')

    from .models import Account, Note
    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return Account.query.get(int(id))
    return app