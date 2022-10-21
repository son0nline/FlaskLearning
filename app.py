import os
from flask import Flask
from flask_smorest import Api
import urllib.request

from db.sqlcontext import db
import models

from dotenv import load_dotenv
# python-dotenv read file .env
load_dotenv()

from controllers.items import blp as ItemBlueprint
from controllers.stores import blp as StoreBlueprint
from controllers.tag import blp as TagBlueprint

def getDbConnectString(db_url=None)->str:
    params = urllib.parse.quote_plus(os.environ.get('DBCONNECT'))
    # need pip install pyodbc
    sqlServerConnectString = "mssql+pyodbc:///?odbc_connect=%s" % params
    
    sqliteConnectString = "sqlite:///data.db"

    return db_url or sqlServerConnectString or sqliteConnectString

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
    app.config["SQLALCHEMY_DATABASE_URI"] = getDbConnectString(db_url)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return f"Hello, Flask world! {__name__}\n"
    
    return app