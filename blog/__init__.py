from flask import Flask
from .models import db,UserModel,PostModel
from flask_migrate import Migrate
from .admin import AdminUserView,AdminPostView
from flask_admin import Admin
from blog import post,auth
from flask_smorest import Api


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    api = Api(app)

    api.register_blueprint(post.bpa)

    app.register_blueprint(auth.bp)
    # app.register_blueprint(post.bp)

    db.init_app(app)
    Migrate(app,db)

    admin = Admin(app,name='Dashboard',template_mode='bootstrap3')
    admin.add_view(AdminUserView(UserModel,db.session))
    admin.add_view(AdminPostView(PostModel,db.session))

    @app.route('/')
    def home():
        return 'Hello'

    return app