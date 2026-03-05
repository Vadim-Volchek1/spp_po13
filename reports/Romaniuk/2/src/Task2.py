from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict


class IAccounting(ABC):

    @abstractmethod
    def calculate_price(self, base_price: float) -> float:
        """Рассчитать цену с налогом."""


class Entity:

    def __init__(self, entity_id: int):
        self.id = entity_id


class Station(Entity):

    def __init__(self, entity_id: int, name: str, city: str):
        super().__init__(entity_id)
        self.name = name
        self.city = city

    def __str__(self) -> str:
        return f"{self.city} - {self.name}"


class Carriage(Entity):

    def __init__(self, entity_id: int, carriage_type: str, seat_count: int):
        super().__init__(entity_id)
        self.carriage_type = carriage_type
        self.seats = []
        for i in range(seat_count):
            self.seats.append(Seat(i + 1))

    def free_seats(self) -> int:
        count = 0
        for seat in self.seats:
            if not seat.is_taken:
                count += 1
        return count


class Seat:

    def __init__(self, number: int):
        self.number = number
        self.is_taken = False

    def take(self) -> None:
        self.is_taken = True


class Train(Entity):

    def __init__(self, entity_id: int, train_number: str):
        super().__init__(entity_id)
        self.train_number = train_number
        self.route = []
        self.prices = {}
        self.carriages = []

    def add_carriage(self, carriage: Carriage) -> None:
        self.carriages.append(carriage)

    def free_seats(self) -> int:
        total = 0
        for carriage in self.carriages:
            total += carriage.free_seats()
        return total


class Passenger(Entity):

    def __init__(self, entity_id: int, name: str, phone: str):
        super().__init__(entity_id)
        self.name = name
        self.phone = phone
        self.requests = []

    def create_request(self, station: Station, date: datetime):
        new_request = Request(len(self.requests) + 1, self, station, date)
        self.requests.append(new_request)
        return new_request


class Request(Entity):

    def __init__(self, entity_id: int, passenger: Passenger, station: Station, date: datetime):
        super().__init__(entity_id)
        self.passenger = passenger
        self.station = station
        self.date = date
        self.status = "новая"

    def __str__(self) -> str:
        return f"заявка {self.id}: {self.passenger.name} -> {self.station.city}"


class Invoice(Entity):

    def __init__(self, entity_id: int, amount: float, passenger: Passenger):
        super().__init__(entity_id)
        self.amount = amount
        self.passenger = passenger
        self.is_paid = False

    def __str__(self) -> str:
        return f"счет {self.id} на {self.amount} руб"


class SimpleAccounting(IAccounting):

    def calculate_price(self, base_price: float) -> float:
        return base_price * 1.13


class Administrator:

    def __init__(self, system: "RailwayTicketSystem"):
        self.system = system

    def add_station(self, name: str, city: str) -> Station:
        station = Station(len(self.system.stations) + 1, name, city)
        self.system.stations.append(station)
        return station

    def add_train(self, number: str, route: List[Station], prices: Dict[str, float]) -> Train:
        train = Train(len(self.system.trains) + 1, number)
        train.route = route
        train.prices = prices
        train.add_carriage(Carriage(1, "купе", 36))
        train.add_carriage(Carriage(2, "плацкарт", 54))
        self.system.trains.append(train)
        print(f"поезд {number} добавлен")
        return train


class RailwayTicketSystem:

    def __init__(self):
        self.trains = []
        self.stations = []
        self.passengers = []
        self.requests = []
        self.invoices = []
        self.accounting = SimpleAccounting()
        self.admin = Administrator(self)

    def register_passenger(self, name: str, phone: str) -> Passenger:
        passenger = Passenger(len(self.passengers) + 1, name, phone)
        self.passengers.append(passenger)
        return passenger

    def find_trains(self, request_obj: Request) -> List[Train]:
        suitable = []
        for train in self.trains:
            if request_obj.station in train.route:
                suitable.append(train)
        return suitable

    def book_ticket(self, passenger_obj: Passenger, train_obj: Train) -> Optional[Invoice]:
        if train_obj.free_seats() <= 0:
            return None

        for carriage in train_obj.carriages:
            for seat in carriage.seats:
                if not seat.is_taken:
                    seat.take()
                    base = train_obj.prices.get(carriage.carriage_type, 1000)
                    total = self.accounting.calculate_price(base)
                    invoice = Invoice(len(self.invoices) + 1, total, passenger_obj)
                    self.invoices.append(invoice)
                    return invoice
        return None


def main():
    print("ЖЕЛЕЗНОДОРОЖНАЯ КАССА")

    system = RailwayTicketSystem()

    brest = system.admin.add_station("брестский вокзал", "Брест")
    minsk = system.admin.add_station("минск вокзал", "Минск")
    vitebsk = system.admin.add_station("вокзал", "Витебск")

    print("\nстанции добавлены:")

    train1 = system.admin.add_train("101", [brest, minsk, vitebsk], {"купе": 50, "плацкарт": 30})
    train2 = system.admin.add_train("202", [brest, minsk], {"купе": 20, "плацкарт": 12})

    ivan = system.register_passenger("иван петров", "+375292563625")
    print(f"\nпассажир: {ivan.name}")

    request_obj = ivan.create_request(brest, datetime(2025, 3, 10))
    system.requests.append(request_obj)
    print(f"создана: {request_obj}")

    trains = system.find_trains(request_obj)
    print(f"найдено поездов: {len(trains)}")
    for train in trains:
        print(f"  поезд {train.train_number}, " f"свободных мест: {train.free_seats()}")

    invoice_obj = system.book_ticket(ivan, train1)
    if invoice_obj:
        print(f"\n{invoice_obj}")
        print(f"осталось мест в поезде: {train1.free_seats()}")
    else:
        print("\nнет свободных мест") 


if __name__ == "__main__":
    main()
