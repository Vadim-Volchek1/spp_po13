from datetime import datetime


class Entity:
    def __init__(self, entity_id):
        self.entity_id = entity_id


class Station(Entity):
    def __init__(self, entity_id, name, city):
        super().__init__(entity_id)
        self.name = name
        self.city = city

    def __str__(self):
        return f"{self.city} - {self.name}"


class Seat:
    def __init__(self, number):
        self.number = number
        self.is_taken = False

    def take(self):
        self.is_taken = True


class Carriage:
    def __init__(self, carriage_id, carriage_type, seat_count):
        self.carriage_id = carriage_id
        self.carriage_type = carriage_type
        self.seats = [Seat(i + 1) for i in range(seat_count)]

    def free_seats(self):
        count = 0
        for seat in self.seats:
            if not seat.is_taken:
                count += 1
        return count


class Train(Entity):
    def __init__(self, entity_id, number):
        super().__init__(entity_id)
        self.number = number
        self.route = []
        self.prices = {}
        self.carriages = []

    def add_carriage(self, carriage):
        self.carriages.append(carriage)

    def free_seats(self):
        total = 0
        for carriage in self.carriages:
            total += carriage.free_seats()
        return total


class Passenger(Entity):
    def __init__(self, entity_id, name, phone):
        super().__init__(entity_id)
        self.name = name
        self.phone = phone
        self.requests = []

    def create_request(self, station, date):
        req = Request(len(self.requests) + 1, self, station, date)
        self.requests.append(req)
        return req


class Request(Entity):
    def __init__(self, entity_id, passenger, station, date):
        super().__init__(entity_id)
        self.passenger = passenger
        self.station = station
        self.date = date
        self.status = "новая"

    def __str__(self):
        return f"заявка {self.entity_id}: {self.passenger.name} -> {self.station.city}"


class Invoice(Entity):
    def __init__(self, entity_id, amount, passenger):
        super().__init__(entity_id)
        self.amount = amount
        self.passenger = passenger
        self.is_paid = False

    def __str__(self):
        return f"счет {self.entity_id} на {self.amount} руб"


class RailwaySystem:
    def __init__(self):
        self.trains = []
        self.stations = []
        self.passengers = []
        self.requests = []
        self.invoices = []
        self.next_id = 1

    def add_station(self, name, city):
        station = Station(self.next_id, name, city)
        self.stations.append(station)
        self.next_id += 1
        return station

    def add_train(self, number, route, prices):
        train = Train(self.next_id, number)
        train.route = route
        train.prices = prices
        train.add_carriage(Carriage(1, "купе", 36))
        train.add_carriage(Carriage(2, "плацкарт", 54))
        self.trains.append(train)
        self.next_id += 1
        print(f"поезд {number} добавлен")
        return train

    def register_passenger(self, name, phone):
        passenger = Passenger(self.next_id, name, phone)
        self.passengers.append(passenger)
        self.next_id += 1
        return passenger

    def find_trains(self, station):
        suitable = []
        for train in self.trains:
            if station in train.route:
                suitable.append(train)
        return suitable

    def book_ticket(self, passenger, train, carriage_type="купе"):
        if train.free_seats() <= 0:
            return None

        for carriage in train.carriages:
            if carriage.carriage_type == carriage_type:
                for seat in carriage.seats:
                    if not seat.is_taken:
                        seat.take()
                        price = train.prices.get(carriage_type, 1000)
                        total = price * 1.13
                        invoice = Invoice(self.next_id, total, passenger)
                        self.invoices.append(invoice)
                        self.next_id += 1
                        return invoice
        return None


def main():
    print("ЖЕЛЕЗНОДОРОЖНАЯ КАССА\n")

    system = RailwaySystem()

    brest = system.add_station("брестский вокзал", "Брест")
    minsk = system.add_station("минск вокзал", "Минск")
    vitebsk = system.add_station("вокзал", "Витебск")
    print("станции добавлены")

    train1 = system.add_train("101", [brest, minsk, vitebsk], {"купе": 50, "плацкарт": 30})
    system.add_train("202", [brest, minsk], {"купе": 20, "плацкарт": 12})

    ivan = system.register_passenger("иван петров", "+375292563625")
    print(f"\nпассажир: {ivan.name}")

    request = ivan.create_request(brest, datetime(2025, 3, 10))
    system.requests.append(request)
    print(f"создана: {request}")

    trains = system.find_trains(brest)
    print(f"найдено поездов: {len(trains)}")
    for train in trains:
        print(f"  поезд {train.number}, свободных мест: {train.free_seats()}")

    invoice = system.book_ticket(ivan, train1, "купе")
    if invoice:
        print(f"\n{invoice}")
        print(f"осталось мест в поезде: {train1.free_seats()}")
    else:
        print("\nнет свободных мест")


if __name__ == "__main__":
    main()
