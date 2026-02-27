class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Client:
    def __init__(self, name, many):
        self.name = name
        self.many = many
        self.blacklisted = False

    def pay(self, amount):
        self.many -= amount


class Order:
    def __init__(self, client):
        self.client = client
        self.products = []
        self.paid = False

    def add_product(self, product):
        if not self.client.blacklisted:
            self.products.append(product)

    def total_price(self):
        total = 0
        for product in self.products:
            total += product.price
        return total

    def pay(self):
        if self.client.many >= self.total_price():
            self.client.pay(self.total_price())
            self.paid = True
            return True
        return False


class Store:
    def __init__(self):
        self.products = []
        self.sales = []
        self.black_list = []

    def add_product(self, product):
        self.products.append(product)

    def register_sale(self, order):
        if order.paid:
            self.sales.append(order)
        else:
            order.client.blacklisted = True
            self.black_list.append(order.client)


store = Store()

p1 = Product("Телефон", 30000)
p2 = Product("Ноутбук", 80000)

store.add_product(p1)
store.add_product(p2)

client = Client("Иван", 50000)
client2 = Client("Иванов", 100000)

order = Order(client)
order.add_product(p1)
order.add_product(p2)

if order.pay():
    print("Заказ оплачен. Сумма:", order.total_price())
else:
    print("Клиент в черном списке")

store.register_sale(order)

order2 = Order(client2)
order2.add_product(p1)
if order2.pay():
    print("Заказ оплачен. Сумма:", order2.total_price())
else:
    print("Клиент в черном списке")

store.register_sale(order2)

print("Количество продаж:", len(store.sales))
print("Черный список:", [c.name for c in store.black_list])
