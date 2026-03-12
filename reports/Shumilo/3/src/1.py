from abc import ABC, abstractmethod

class Burger:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Drink:
    def __init__(self, name: str, price: float, is_hot: bool):
        self.name = name
        self.price = price
        self.is_hot = is_hot


class Packing:
    def __init__(self, name: str, extra_cost: float = 0.0):
        self.name = name
        self.extra_cost = extra_cost


class Order:
    def __init__(self):
        self.burger: Burger | None = None
        self.drink: Drink | None = None
        self.packing: Packing | None = None

    @property
    def total_price(self) -> float:
        total = 0.0
        if self.burger:
            total += self.burger.price
        if self.drink:
            total += self.drink.price
        if self.packing:
            total += self.packing.extra_cost
        return total

    def __str__(self) -> str:
        lines = ["Ваш заказ:"]
        if self.burger:
            lines.append(f"Бургер: {self.burger.name} (цена: {self.burger.price})")
        if self.drink:
            lines.append(f"Напиток: {self.drink.name} (цена: {self.drink.price})")
        if self.packing:
            lines.append(
                f"Упаковка: {self.packing.name} (доплата: {self.packing.extra_cost})"
            )
        lines.append(f"Итого: {self.total_price}")
        return "\n".join(lines)

class OrderBuilder(ABC):
    def __init__(self):
        self._order = Order()

    @abstractmethod
    def build_burger(self, burger_type: int) -> None:
        pass

    @abstractmethod
    def build_drink(self, drink_type: int) -> None:
        pass

    @abstractmethod
    def build_packing(self, packing_type: int) -> None:
        pass

    def get(self) -> Order:
        return self._order


class SimpleOrderBuilder(OrderBuilder):
    def build_burger(self, burger_type: int) -> None:
        if burger_type == 1:
            self._order.burger = Burger("Веганский бургер", 10.0)
        elif burger_type == 2:
            self._order.burger = Burger("Куриный бургер", 12.0)
        elif burger_type == 3:
            self._order.burger = Burger("Говяжий бургер", 15.0)
        else:
            raise ValueError("Неизвестный тип бургера")

    def build_drink(self, drink_type: int) -> None:
        if drink_type == 1:
            self._order.drink = Drink("Пепси", 5.0, is_hot=False)
        elif drink_type == 2:
            self._order.drink = Drink("Кока-кола", 5.0, is_hot=False)
        elif drink_type == 3:
            self._order.drink = Drink("Кофе", 6.0, is_hot=True)
        elif drink_type == 4:
            self._order.drink = Drink("Чай", 4.0, is_hot=True)
        else:
            raise ValueError("Неизвестный тип напитка")

    def build_packing(self, packing_type: int) -> None:
        if packing_type == 1:
            self._order.packing = Packing("С собой", extra_cost=1.0)
        elif packing_type == 2:
            self._order.packing = Packing("На месте", extra_cost=0.0)
        else:
            raise ValueError("Неизвестный тип упаковки")



print("Бургер-закусочная")
while True:
    print("\nСоздание нового заказа...")
    builder = SimpleOrderBuilder()
    print("Выберите бургер: 1 - веганский, 2 - куриный, 3 - говяжий")
    burger_t = int(input("Ваш выбор: "))
    builder.build_burger(burger_t)
    print("Выберите напиток: 1 - пепси, 2 - кока-кола, 3 - кофе, 4 - чай")
    drink_t = int(input("Ваш выбор: "))
    builder.build_drink(drink_t)
    print("Выберите упаковку: 1 - с собой, 2 - на месте")
    packing_t = int(input("Ваш выбор: "))
    builder.build_packing(packing_t)

    order = builder.get()
    print("\n" + str(order))

    print("\nХотите сделать ещё один заказ? (y/n)")
    again = input("Ваш выбор: ").strip().lower()

    if again != "y":
        break

