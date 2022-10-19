from uuid import UUID, uuid4, uuid5


items = {
    "9ef353993ea74adaa5a741a118607dc2": {
        "id": "9ef353993ea74adaa5a741a118607dc2",
        "name": "chair",
        "price": 15.99,
        "store_id": "2e69ae110dc44033a6443a3ee3d2cf1e"
    },
    "9ef353993ea74adaa5a741a118607dc3": {
        "id": "9ef353993ea74adaa5a741a118607dc3",
        "name": "chair",
        "price": 15.99,
        "store_id": "2e69ae110dc44033a6443a3ee3d2cf1e"
    },
}

print(items.values())


uId = uuid4().hex
print(uId)

for id in items:
    print(id, items[id]["store_id"])

store_items = [items[id] for id in items if items[id]
               ["store_id"] == "2e69ae110dc44033a6443a3ee3d2cf1e"]
print(len(store_items))
