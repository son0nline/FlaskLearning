from flask import Flask

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
    
@app.get("/store")
def get_store():
    return {"stores": stores}