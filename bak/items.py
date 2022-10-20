from uuid import uuid4
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from bak.db import items
from bak.db import stores

from db.schemas import BaseRsp, ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):

    @blp.arguments(ItemSchema)
    def post(self,item_data):
        # sẽ lấy từ argument nên không cần đọc request 
        #item_data = request.get_json()

        if item_data["store_id"] not in stores:
            abort(404, message="store not found")

        item_id = uuid4().hex
        new_item = {"id": item_id, **item_data}
        items[item_id] = new_item
        return new_item, 201
    
    def get(self):
        return {"items": list(items.values())}

@blp.route("/item/<item_id>")
class ItemInfo(MethodView):
    
    @blp.response(200,ItemSchema)
    @blp.response(500,BaseRsp)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return {"message": "item not found"}, 404
        except:
            return {"message": "sys error"}, 500
    
    @blp.arguments(ItemUpdateSchema) 
    def put(self, item_data, item_id): # chú ý json phải để trước các thứ khác
        #item_data = request.get_json()
        item = items[item_id]
        item |= item_data
        return item_data, 202

    def delete(self, item_id):
        if items.get(item_id) != None:
            del items[item_id]
            return {"message":"Item deleted!"}
        
        return {"message":"Item not found!"}