from operator import truediv
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bak.db import stores
from db.schemas import BaseRsp, StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        #store_data = request.get_json()

        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        #return {"stores": list(stores.values())}
        return stores.values()

@blp.route("/store/<string:store_id>")
class StoreInfo(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")


    @blp.response(200, BaseRsp)
    @blp.response(404, BaseRsp)
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")

