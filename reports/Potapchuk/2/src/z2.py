from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Product:
    name: str
    price: float


@dataclass
class User:
    name: str


@dataclass
class Customer(User):
    balance: float = 0.0
    is_blacklisted: bool = False


@dataclass
class Administrator(User):
    pass


@dataclass
class Order:
    customer: Customer
    products: List[Product] = None

    def __post_init__(self):
        if self.products is None:
            self.products = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def total_cost(self) -> float:
        return sum(p.price for p in self.products)


@dataclass
class Store:
    admin: Administrator
    catalog: List[Product]
    sales: List[Order] = None

    def __post_init__(self):
        if self.sales is None:
            self.sales = []

    def register_sale(self, order: Order) -> None:
        if order.customer.is_blacklisted:
            print(f"Customer {order.customer.name} is blacklisted. Sale rejected.")
            return

        total = order.total_cost()
        if order.customer.balance < total:
            print(f"Customer {order.customer.name} has insufficient funds "
                  f"({order.customer.balance} < {total}).")
            return

        order.customer.balance -= total
        self.sales.append(order)
        print(f"Sale registered for {order.customer.name}. Total: {total}")


def pay(self: Customer, amount: float) -> bool:
    if amount <= 0:
        print("Amount must be positive.")
        return False
    if self.balance >= amount:
        self.balance -= amount
        print(f"Payment successful. New balance: {self.balance}")
        return True
    else:
        print(f"Insufficient funds. Need {amount}, have {self.balance}")
        return False


Customer.pay = pay  


def main():
    admin = Administrator(name="Admin Alex")
    catalog = [
        Product(name="Laptop", price=1200.0),
        Product(name="Mouse", price=25.0),
        Product(name="Keyboard", price=60.0),
        Product(name="Monitor", price=280.0),
    ]

    store = Store(admin=admin, catalog=catalog)

    customers = [
        Customer(name="Anna", balance=1500.0),
        Customer(name="Boris", balance=40.0),
        Customer(name="Clara", balance=800.0),
    ]

    print("=== Store catalog ===")
    for item in catalog:
        print(f"  {item.name:12}  ${item.price:6.2f}")

    print("\n=== Starting sales simulation ===")

    order1 = Order(customer=customers[0])
    order1.add_product(catalog[0])          
    order1.add_product(catalog[1])           
    store.register_sale(order1)

    order2 = Order(customer=customers[1])
    order2.add_product(catalog[0])           
    store.register_sale(order2)

    order3 = Order(customer=customers[2])
    order3.add_product(catalog[2])           
    order3.add_product(catalog[3])           
    store.register_sale(order3)

    customers[1].is_blacklisted = True
    print(f"\nCustomer {customers[1].name} blacklisted.")

    order4 = Order(customer=customers[1])
    order4.add_product(catalog[1])           
    store.register_sale(order4)

    print("\n=== Final balances ===")
    for c in customers:
        print(f"  {c.name:8}  balance: ${c.balance:6.2f}  blacklisted: {c.is_blacklisted}")


if __name__ == "__main__":
    main()
