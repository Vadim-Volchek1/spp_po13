"""Store management system."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Product:
    """Product data model."""

    name: str
    price: float


@dataclass
class User:
    """Base user class."""

    name: str


@dataclass
class Customer(User):
    """Customer class with balance and blacklist status."""

    balance: float = 0.0
    is_blacklisted: bool = False

    def pay(self, amount: float) -> bool:
        """Process payment and update balance."""
        if amount <= 0:
            print("Amount must be positive.")
            return False

        if self.balance >= amount:
            self.balance -= amount
            print(f"Payment successful. New balance: {self.balance}")
            return True

        print(f"Insufficient funds. Need {amount}, have {self.balance}")
        return False


@dataclass
class Administrator(User):
    """Administrator user class."""


@dataclass
class Order:
    """Order class containing customer and product list."""

    customer: Customer
    products: Optional[List[Product]] = None

    def __post_init__(self):
        if self.products is None:
            self.products = []

    def add_product(self, product: Product) -> None:
        """Add a product to the order."""
        self.products.append(product)

    def total_cost(self) -> float:
        """Calculate the total price of the order."""
        return sum(p.price for p in self.products)


@dataclass
class Store:
    """Store class handling catalog and sales registration."""

    admin: Administrator
    catalog: List[Product]
    sales: Optional[List[Order]] = None

    def __post_init__(self):
        if self.sales is None:
            self.sales = []

    def register_sale(self, order: Order) -> None:
        """Validate and register a sale."""
        if order.customer.is_blacklisted:
            print(f"Customer {order.customer.name} is blacklisted. Sale rejected.")
            return

        total = order.total_cost()

        if order.customer.balance < total:
            print(f"Customer {order.customer.name} has insufficient funds " f"({order.customer.balance} < {total}).")
            return

        order.customer.balance -= total
        self.sales.append(order)
        print(f"Sale registered for {order.customer.name}. Total: {total}")


def main():
    """Main execution logic for store simulation."""
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
    for customer in customers:
        print(f"  {customer.name:8}  balance: ${customer.balance:6.2f}  " f"blacklisted: {customer.is_blacklisted}")


if __name__ == "__main__":
    main()
