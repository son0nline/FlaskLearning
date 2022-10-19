from datetime import datetime
import re

from uuid import uuid4
from flask import Flask, request
from flask_smorest import abort

from db.db import stores, items

app = Flask(__name__)


@app.route("/")
def home():
    return f"Hello, Flask! {__name__}"


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)


@app.route("/hello/<name>")
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

# @app.route("/store", methods=["GET"])
#  is equal @app.get("/store")


@app.get("/store")
def get_store():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    # json equal to python dictionary
    rq_data = request.get_json()
    store_id = uuid4().hex
    new_store = {"id": store_id,  **rq_data}
    stores[store_id] = new_store
    return new_store, 201  # 201 is http_status CREATED


@app.get("/store/<string:store_id>")
def search_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="store not found")
    except:
        return {"message": "sys error"}, 500


@app.get("/store/<string:store_id>/items")
def get_item_in_store(store_id):
    store_items = [items[id]
                for id in items if items[id]["store_id"] == store_id]
    return { "store_id": store_id,
        "items": store_items}, 200    


@app.post("/item")
def create_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        abort(404, message="store not found")

    item_id = uuid4().hex
    new_item = {"id": item_id, **item_data}
    items[item_id] = new_item
    return new_item, 201


@app.get("/item")
def get_all_item():
    return {"items": list(items.values())}


@app.get("/item/<item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "item not found"}, 404
    except:
        return {"message": "sys error"}, 500
