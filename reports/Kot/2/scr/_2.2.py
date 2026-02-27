from abc import ABC, abstractmethod
class Transport(ABC):
    def __init__(self, number):
        self.number = number
        self.route = None
        self.is_working = True
    def assign_route(self, route):
        self.route = route
    def breakdown(self):
        self.is_working = False
        print(f"{self} is broken")
        if self.route:
            self.route.handle_breakdown(self)
    @abstractmethod
    def move(self):
        pass
    def __str__(self):
        return f"{self.__class__.__name__} #{self.number}"
class Bus(Transport):
    def move(self):
        print(f"{self} moves on route {self.route.number}")
class Trolleybus(Transport):
    def move(self):
        print(f"{self} moves on route {self.route.number}")
class Route:
    def __init__(self, number, interval):
        self.number = number
        self.interval = interval
        self.transports = []
        self.reserve = []
    def add_transport(self, transport):
        transport.assign_route(self)
        self.transports.append(transport)
    def add_reserve(self, transport):
        self.reserve.append(transport)
        print(f"Reserve {transport} added to route {self.number}")
    def handle_breakdown(self, transport):
        if transport in self.transports:
            self.transports.remove(transport)
            transport.is_working = False
            if self.reserve:
                reserve_transport = self.reserve.pop(0)
                reserve_transport.assign_route(self)
                self.transports.append(reserve_transport)
                print(f"Reserve {reserve_transport} assigned to route")
            else:
                self.interval += 5
                print(f"No reserve available. Interval increased to {self.interval}")            
    def show_status(self):
        print(f"\n=== Route {self.number} ===")
        print(f"Interval: {self.interval} minutes")
        print("Active transports:")
        for t in self.transports:
            status = "working" if t.is_working else "broken"
            print(f"  {t} - {status}")
        if self.reserve:
            print("Reserve transports:")
            for r in self.reserve:
                print(f"  {r}")
route1 = Route(10, 15)
bus1 = Bus(101)
trolley1 = Trolleybus(201)
reserve_bus = Bus(999)
route1.add_transport(bus1)
route1.add_transport(trolley1)
route1.add_reserve(reserve_bus)
route1.show_status()
bus1.move()
trolley1.move()
bus1.breakdown()
route1.show_status()
trolley1.breakdown()
route1.show_status()
