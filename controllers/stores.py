from sqlite3 import IntegrityError

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db.sqlcontext import db
from db.schemas import BaseRsp, ItemSchema, PlainItemSchema, PlainStoreSchema, StoreSchema

from sqlalchemy.exc import SQLAlchemyError
from models import StoreModel
from sqlalchemy.sql import text

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store")
class Store(MethodView):

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store

    @blp.response(200, PlainStoreSchema(many=True))
    def get(self):
        #return {"stores": list(stores.values())}
        rs = db.session.execute('SELECT * FROM stores')
        return rs

@blp.route("/store/<string:store_id>")
class StoreInfo(MethodView):
    
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store


    @blp.response(200, BaseRsp)
    @blp.response(404, BaseRsp)
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200

@blp.route("/store/<store_id>/items")
class StoreItemsInfo(MethodView):
    
    #@blp.response(200, StoreSchema)
    @blp.response(200, PlainItemSchema(many=True)) # đây sẽ mô tả dữ liệu trả về
    def get(self, store_id):
        
        if StoreModel.query.filter(StoreModel.id == store_id).first() == None:
            return {"message":"store not found!"},404

        rsItems = StoreModel.query.filter(StoreModel.id == store_id)
        
        for row in rsItems.all():
            print(type(row))

        # store = db.session.execute('SELECT * FROM stores where id=:val', {'val': store_id})
        rs_query = db.session.execute('SELECT id,name,price FROM items where store_id=:val', {'val': store_id})
        # không [select * ] bởi vì PlainItemSchema không có mô tả trường store_id
        # nếu object trả về có trường đó sẽ lỗi
                
        # for row in rs_query:
        #     print(row, type(row), dict(row))
        #     return dict(row)
        return [dict(row) for row in rs_query] 
        #@blp.response(200, PlainItemSchema(many=True))

        #@blp.response(200, StoreSchema)
        return StoreModel.query.get_or_404(store_id)
        return {"message":"error"}
