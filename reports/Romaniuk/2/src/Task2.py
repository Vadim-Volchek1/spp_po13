from datetime import datetime
from typing import List, Optional, Dict, Tuple


class TicketStatus:
    PENDING = "Ожидает оплаты"
    PAID = "Оплачен"


class Station:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Train:
    def __init__(self, num: str):
        self.train_number = num
        self.route: List[Station] = []
        self.prices: Dict[Tuple[str, str], float] = {}

    def add_station(self, s: Station) -> None:
        self.route.append(s)

    def set_price(self, f: Station, t: Station, p: float) -> None:
        self.prices[(f.name, t.name)] = p

    def get_price(self, f: Station, t: Station) -> Optional[float]:
        return self.prices.get((f.name, t.name))

    def __str__(self):
        st = " -> ".join([s.name for s in self.route])
        return f"Поезд №{self.train_number}: {st}"


class Trip:
    def __init__(self, tr: Train, d: str, tm: str):
        self.train = tr
        self.date = d
        self.time = tm
        self.seats = 50

    def __str__(self):
        return f"Рейс {self.train.train_number} | " f"{self.date} {self.time} | Мест: {self.seats}"


class Request:
    def __init__(self, p: "Passenger", dest: str):
        self.passenger = p
        self.destination = dest
        self.processed = False
        self.trips: List[Trip] = []


class InvData:
    def __init__(self, data: tuple):
        self.passenger = data[0]
        self.trip = data[1]
        self.amount = data[2]
        self.frm = data[3]
        self.to = data[4]


class Invoice:
    def __init__(self, d: InvData):
        self.passenger = d.passenger
        self.trip = d.trip
        self.amount = d.amount
        self.frm = d.frm
        self.to = d.to
        self.status = TicketStatus.PENDING
        self.created = datetime.now()

    def pay(self) -> None:
        self.status = TicketStatus.PAID
        self.trip.seats -= 1
        print(f"Счет оплачен. Статус: {self.status}")

    def __str__(self):
        return (
            f"Счет: {self.trip.date} {self.trip.time} "
            f"{self.frm}->{self.to} = {self.amount} руб. "
            f"Статус: {self.status}"
        )


class Passenger:
    def __init__(self):
        self.reqs: List[Request] = []

    def create_request(self, d: str) -> Request:
        r = Request(self, d)
        self.reqs.append(r)
        return r


class Admin:
    def __init__(self, login: str):
        self.login = login

    def add_train(self, sys: "RailwaySystem", num: str) -> Train:
        return sys.add_train(num)

    def cfg_train(self, t: Train, st: List[str], pr: Dict[Tuple[int, int], float]) -> None:
        objs = []
        for name in st:
            obj = Station(name)
            t.add_station(obj)
            objs.append(obj)
        for (fi, ti), val in pr.items():
            t.set_price(objs[fi], objs[ti], val)
        print(f"Админ {self.login} настроил поезд {t.train_number}")

    def add_trip(self, sys: "RailwaySystem", t: Train, d: str, tm: str) -> Trip:
        return sys.add_trip(t, d, tm)


class RailwaySystem:
    def __init__(self):
        self.trains: List[Train] = []
        self.trips: List[Trip] = []
        self.reqs: List[Request] = []
        self.invs: List[Invoice] = []

    def add_train(self, num: str) -> Train:
        t = Train(num)
        self.trains.append(t)
        return t

    def add_trip(self, t: Train, d: str, tm: str) -> Trip:
        tr = Trip(t, d, tm)
        self.trips.append(tr)
        return tr

    def reg_req(self, r: Request) -> None:
        self.reqs.append(r)
        r.processed = True

    def search(self, r: Request, frm: str, to_: str) -> List[Trip]:
        found = []
        for tr in self.trips:
            trn = tr.train
            names = [s.name for s in trn.route]
            if frm in names and to_ in names:
                fi = names.index(frm)
                ti = names.index(to_)
                if fi < ti and tr.seats > 0:
                    found.append(tr)
        r.trips = found
        return found

    def choose(self, r: Request, tr: Trip, frm: str, to_: str) -> Optional[Invoice]:
        trn = tr.train
        f_obj = None
        t_obj = None
        for s in trn.route:
            if s.name == frm:
                f_obj = s
            if s.name == to_:
                t_obj = s
        if f_obj is None or t_obj is None:
            return None
        price = trn.get_price(f_obj, t_obj)
        if price is None:
            return None
        data_tuple = (r.passenger, tr, price, f_obj, t_obj)
        d = InvData(data_tuple)
        inv = Invoice(d)
        self.invs.append(inv)
        return inv


def fmt_row(tr: Trip, f: str, t: str, i: int) -> str:
    trn = tr.train
    names = [s.name for s in trn.route]
    fi = names.index(f)
    ti = names.index(t)
    fo = trn.route[fi]
    to = trn.route[ti]
    p = trn.get_price(fo, to)
    r = f"{f}->{t}"
    return f"{i}. {trn.train_number} {tr.date} " f"{tr.time} {r:15} {p:6} руб. " f"{tr.seats:3}"


def print_tkt(inv: Invoice, tr: Trip, f: str, t: str) -> None:
    print("\n" + "=" * 50)
    print("                БИЛЕТ КУПЛЕН")
    print("=" * 50)
    print(f"Поезд: {tr.train.train_number}")
    print(f"Дата: {tr.date}")
    print(f"Время: {tr.time}")
    print(f"Маршрут: {f} -> {t}")
    print(f"Цена: {inv.amount} руб.")
    print(f"Мест: {tr.seats}")
    print("=" * 50)


def get_stations(sys: RailwaySystem) -> List[str]:
    res = []
    for t in sys.trains:
        for s in t.route:
            if s.name not in res:
                res.append(s.name)
    return res


def show_stations(ss: List[str]) -> None:
    print("\nСтанции:")
    for i, s in enumerate(ss):
        print(f"{i+1}. {s}")


def pick_station(ss: List[str], msg: str, ex: int = -1) -> Tuple[int, str]:
    ch = int(input(msg)) - 1
    if ch < 0 or ch >= len(ss):
        raise ValueError("Неверный номер")
    if ch == ex:
        raise ValueError("Станции должны быть разными")
    return ch, ss[ch]


def buy_proc(sys: RailwaySystem, u: Passenger, f: str, t: str, trips: List[Trip]) -> bool:
    print(f"\nРейсов: {len(trips)}")
    print("-" * 90)
    print("№  Поезд   Дата       Время   Маршрут          Цена   Места")
    print("-" * 90)

    for i, tr in enumerate(trips):
        print(fmt_row(tr, f, t, i + 1))

    ch = int(input("\nВыберите рейс (номер): ")) - 1
    if ch < 0 or ch >= len(trips):
        print("Неверный номер!")
        return False

    tr = trips[ch]
    r = u.create_request(t)
    sys.reg_req(r)
    inv = sys.choose(r, tr, f, t)

    if inv:
        print(f"\n{inv}")
        pay = input("Оплатить? (1 - да, 0 - нет): ")
        if pay == "1":
            inv.pay()
            print_tkt(inv, tr, f, t)
        else:
            print("Отмена")
    return True


def setup():
    sys = RailwaySystem()
    adm = Admin("ГлавныйАдмин")
    print("=== НАСТРОЙКА ===")

    t1 = adm.add_train(sys, "101A")
    adm.cfg_train(t1, ["Минск", "Брест", "Гродно"], {(0, 1): 80, (0, 2): 120, (1, 2): 60})

    t2 = adm.add_train(sys, "202B")
    adm.cfg_train(t2, ["Минск", "Орша", "Витебск"], {(0, 1): 45, (0, 2): 90, (1, 2): 50})

    t3 = adm.add_train(sys, "303C")
    adm.cfg_train(t3, ["Гомель", "Могилев", "Минск"], {(0, 1): 50, (0, 2): 100, (1, 2): 60})

    trips = [
        (t1, "2026-04-15", "08:30"),
        (t1, "2026-04-15", "16:45"),
        (t2, "2026-04-15", "10:15"),
        (t2, "2026-04-16", "09:30"),
        (t3, "2026-04-15", "14:20"),
        (t3, "2026-04-16", "11:40"),
        (t1, "2026-04-16", "18:30"),
    ]

    for tr, d, tm in trips:
        adm.add_trip(sys, tr, d, tm)

    print("Готово!")
    return sys


def main():
    sys = setup()
    user = Passenger()

    while True:
        try:
            print("\n" + "=" * 70)
            print("         Беларуская чыгунка")
            print("=" * 70)

            sts = get_stations(sys)
            show_stations(sts)

            fc, f = pick_station(sts, "\nОтправление (номер): ")
            _, t = pick_station(sts, "Назначение (номер): ", fc)

            r = user.create_request(t)
            sys.reg_req(r)
            trips = sys.search(r, f, t)

            if trips:
                buy_proc(sys, user, f, t, trips)
            else:
                print(f"\nНет рейсов {f} -> {t}")

            again = input("\nЕще? (1 - да, 0 - нет): ")
            if again != "1":
                print("\nПока!")
                break

        except ValueError as e:
            print(f"Ошибка! {e}")
        except KeyboardInterrupt:
            print("\n\nПока!")
            break


if __name__ == "__main__":
    main()
