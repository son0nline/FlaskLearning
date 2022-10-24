import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from flask_migrate import Migrate

import urllib.request

from db.sqlcontext import db
from db.blocklist import BLOCKLIST
import models

from dotenv import load_dotenv
# python-dotenv read file .env
load_dotenv()

from controllers.user import blp as UserBlueprint
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

    migrate = Migrate(app,db)

    api = Api(app)




    app.config["JWT_SECRET_KEY"] = 'c19f9578-6c49-4861-9078-d10771855abf'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    # https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # using sqlalchemy to create table
    # can remove when use flask-migrate
    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    
    return app