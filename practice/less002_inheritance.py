class Device:
    def __init__(self, name, connected_by):
        self.name = name
        self.connected_by = connected_by
        self.connected = True
    
    def __str__(self) -> str:
        # de heo! !r meanning quote self.name by single quote
        return f"Device {self.name!r} ({self.connected_by})"
    
    def disconnect(self):
        self.connected = False
        self.connected_by = ""
        print("Disconnected!")

class Printer(Device):

    def __init__(self, name, connected_by,capacity):
        super().__init__(name, connected_by)
        self.capacity = capacity
    
    def __str__(self) -> str:
        return f"{super().__str__()} ({self.capacity})"



d1 = Device("HP","Sony")

print(d1)
