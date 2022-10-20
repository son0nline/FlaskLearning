class Person:
    def __init__(self, name, age) -> None:
        self.Name = name
        self.Age = age
    
    # def __str__(self) -> str:
    #     return (f"Person name: {self.Name}, {self.Age} years old.")

    def __repr__(self) -> str:
        return (f"<class 'Person': ({self.Name}, {self.Age})>")

p1 = Person("robin",20)
print(p1)

class Store:
    def __init__(self,name):
        # You'll need 'name' as an argument to this method.
        # Then, initialise 'self.name' to be the argument, and 'self.items' to be an empty list.
        self.name = name
        self.items = []
    
    def add_item(self, name, price):
        # Create a dictionary with keys name and price, and append that to self.items.
        self.items.append({"name":name, "price":price})

    def stock_price(self):
        # Add together all item prices in self.items and return the total.
        # total = 0
        # for item in self.items:
        #     total += item['price']
        # return total
        return sum([item['price'] for item in self.items])
    
    def instance(self):
        print(f"say my name: {self}")

    @classmethod
    def class_method(cls):
        print(f"say my name: {cls}")

    @classmethod
    def franchise(cls, store):
        # Return another store, with the same name as the argument's name, plus " - franchise"
        newStore = Store(store.name + " - franchise")
        return newStore

    @staticmethod
    def store_details(store):
        # Return a string representing the argument
        # It should be in the format 'NAME, total stock price: TOTAL'
        return f"{store.name}, total stock price: {store.stock_price()}"


s1 = Store("kho1")
s1.add_item("g", 1.5)
s1.add_item("g2", 2.5)
print(s1.stock_price())
s1.instance()

store = Store("Test")
store2 = Store("Amazon")
store2.add_item("Keyboard", 160)
 
Store.franchise(store)  # returns a Store with name "Test - franchise"
Store.franchise(store2)  # returns a Store with name "Amazon - franchise"
 
Store.store_details(store)  # returns "Test, total stock price: 0"
Store.store_details(store2)  # returns "Amazon, total stock price: 160"