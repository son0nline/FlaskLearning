import os
from flask import Flask, request
from datetime import datetime
import re

app = Flask(__name__)

stores = [
    {
        "name" : "my store",
        "items" : [
            { 
                "name": "chair" ,
                "price": 15.99
            },
            { 
                "name": "desk" ,
                "price": 25.99
            },
        ]

    }
]



@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/favicon.ico')
def favicon():
    return Flask.send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)


@app.get("/name")
def get_name():
    return __name__

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

## @app.route("/store", methods=["GET"])
#  is equal @app.get("/store")  
@app.get("/store")
def get_store():
    return {"stores": stores}


@app.post("/store")
def create_store():
    # json equal to python dictionary
    rq_data = request.get_json()
    new_store = {"name":rq_data['name'], "items":[]}
    stores.append(new_store)
    return new_store , 201 # 201 is http_status CREATED

@app.get("/store/<string:name>")
def search_store(name):
    store = [ store if store["name"] == name else None  for store in stores ]
    if store == None or store == [None]:
        return {"message":"store not found"}, 404
    return store,200

@app.post("/store/<string:name>/item")
def create_item(name):
    rq_data = request.get_json()
    new_item = { 
                "name": rq_data['name'] ,
                "price": rq_data['price'] ,
            }

    for store in stores:
        if store["name"] == name:
            store["items"].append(new_item)
        
    return new_item, 201

@app.get("/store/<string:name>/items")
def get_item(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]},200
        
    return {"message":"store not found"}, 204