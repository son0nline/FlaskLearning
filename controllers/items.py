from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db.sqlcontext import db
from db.schemas import BaseRsp, ItemSchema, ItemUpdateSchema

from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel



blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class Item(MethodView):

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
        
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

@blp.route("/item/<item_id>")
class ItemInfo(MethodView):
    
    @blp.response(200,ItemSchema)
    @blp.response(500,BaseRsp)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}