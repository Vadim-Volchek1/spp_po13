from typing import List, Optional


class Product:
    """Product with name and price."""
    
    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"{self.name} ({self.price} руб.)"


class User:
    """Base user class."""
    
    def __init__(self, name: str) -> None:
        self.name = name


class Customer(User):
    """Customer with balance and blacklist status."""
    
    def __init__(self, name: str, balance: int = 0) -> None:
        super().__init__(name)
        self.balance = balance
        self.is_blacklisted = False

    def pay(self, amount: int) -> bool:
        """Deduct amount from balance if enough funds."""
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False


class Admin(User):
    """Admin can add products and blacklist customers."""
    
    def add_product(self, catalog: List[Product], product: Product) -> None:
        """Add product to catalog."""
        catalog.append(product)
        print(f"Админ {self.name}: добавлен товар '{product.name}'")

    def blacklist(self, customer: Customer) -> None:
        """Add customer to blacklist."""
        customer.is_blacklisted = True
        print(f"Админ {self.name}: клиент {customer.name} заблокирован")


class Manager(User):
    """Manager can view sales reports."""
    
    def view_sales(self, shop: 'Shop') -> None:
        """Display all registered sales."""
        if not shop.sales:
            print("Продаж пока нет")
        else:
            print(f"Менеджер {self.name}: просмотр продаж")
            for i, order in enumerate(shop.sales, 1):
                print(f"  {i}. Клиент: {order.customer.name}, Сумма: {order.total_cost()} руб.")


class Order:
    """Customer order containing products."""
    
    def __init__(self, customer: Customer) -> None:
        self.customer = customer
        self.products: List[Product] = []

    def add_product(self, product: Product) -> None:
        """Add product to order."""
        self.products.append(product)

    def total_cost(self) -> int:
        """Calculate total cost of all products."""
        return sum(p.price for p in self.products)


class Shop:
    """Shop with catalog and sales history."""
    
    def __init__(self, admin: Admin) -> None:
        self.admin = admin
        self.catalog: List[Product] = []
        self.sales: List[Order] = []

    def register_sale(self, order: Order) -> None:
        """Process a sale attempt."""
        if order.customer.is_blacklisted:
            print(f"Отказ: клиент {order.customer.name} в чёрном списке.")
            return

        cost = order.total_cost()
        print(f"Попытка оплаты заказа на {cost} руб.")

        if order.customer.pay(cost):
            self.sales.append(order)
            print(f"Успех: продажа оформлена для {order.customer.name}.")
        else:
            print(f"Ошибка: недостаточно средств у {order.customer.name}.")
            self.admin.blacklist(order.customer)


def main() -> None:
    """Main function to run the shop system."""
    try:
        print("=" * 50)
        print("ИНТЕРНЕТ-МАГАЗИН")
        print("=" * 50)
        
        admin_name = input("Имя администратора магазина: ")
        admin = Admin(admin_name)
        shop = Shop(admin)
        
        manager_name = input("Имя менеджера магазина: ")
        manager = Manager(manager_name)

        print("\n--- Добавление товаров (напишите 'стоп' для завершения) ---")
        while True:
            name = input("Название товара: ").strip()
            if name.lower() == "стоп":
                break
            try:
                price = int(input(f"Цена товара '{name}': "))
                if price < 0:
                    print("Цена не может быть отрицательной")
                    continue
                admin.add_product(shop.catalog, Product(name, price))
            except ValueError:
                print("Ошибка: введите целое число для цены")

        if not shop.catalog:
            print("Каталог пуст → завершение программы")
            return

        print("\n--- Оформление заказа ---")
        customer_name = input("Имя клиента: ").strip()
        try:
            money = int(input(f"Сколько денег у {customer_name}? "))
            if money < 0:
                print("Баланс не может быть отрицательным")
                return
        except ValueError:
            print("Ошибка: введите целое число")
            return

        customer = Customer(customer_name, money)
        order = Order(customer)

        print("\nДоступные товары:")
        for i, product in enumerate(shop.catalog):
            print(f"  {i:2d}. {product}")

        user_input = input("\nНомера товаров через пробел (например: 0 2 1): ").strip()
        if not user_input:
            print("Заказ пуст")
            return

        for part in user_input.split():
            try:
                index = int(part)
                if 0 <= index < len(shop.catalog):
                    order.add_product(shop.catalog[index])
                else:
                    print(f"Неверный номер: {part} (игнорируется)")
            except ValueError:
                print(f"Некорректный ввод: {part} (игнорируется)")

        if not order.products:
            print("В заказ ничего не добавлено")
            return

        print("\n--- Результат ---")
        shop.register_sale(order)
        print(f"\nОстаток у клиента {customer.name}: {customer.balance} руб.")
        
        print("\n--- Отчет менеджера ---")
        manager.view_sales(shop)

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
