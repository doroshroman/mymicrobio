from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin 
from flask_ckeditor import CKEditor

db = SQLAlchemy()

def create_app(app):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    bcrypt = Bcrypt(app)
    login = LoginManager(app)
    login.login_view = 'auth.login'
    login.login_message_category = 'info'

    ckeditor = CKEditor(app)

    from app import modelviews
    from app.blueprints.main.views import main
    from app.blueprints.auth.views import auth
    from app.blueprints.posts.views import pb
    from app.blueprints.administrator.views import administrator
    from app.blueprints.account.views import ab
    from app.blueprints.api.views import api
    from flask_admin.contrib.sqla import ModelView
    from app import models

    @login.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))


    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(pb)
    app.register_blueprint(administrator)
    app.register_blueprint(ab)
    app.register_blueprint(api)

    admin = Admin(app, index_view=modelviews.MyAdminIndexView())
    admin.add_view(modelviews.UserAdminView(models.User, db.session))
    admin.add_view(modelviews.PostAdminView(models.Post, db.session))
    
    
    return app
