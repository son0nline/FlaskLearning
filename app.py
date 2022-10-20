import os
from flask import Flask
from flask_smorest import Api


from db.sqlcontext import db
import models

from controllers.items import blp as ItemBlueprint
from controllers.stores import blp as StoreBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    # swagger config
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    ## swagger config
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return f"Hello, Flask world! {__name__}\n"
    
    return app