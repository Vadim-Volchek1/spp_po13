from abc import ABC, abstractmethod


class Product(ABC):
    @abstractmethod
    def get_name(self):
        pass


class Chocolate(Product):
    def get_name(self):
        return "Chocolate bar"


class Chips(Product):
    def get_name(self):
        return "Chips"


class Juice(Product):
    def get_name(self):
        return "Juice"


class ProductFactory:
    @staticmethod
    def create_product(product_type):
        if product_type == "chocolate":
            return Chocolate()
        if product_type == "chips":
            return Chips()
        if product_type == "juice":
            return Juice()
        return None


class VendingMachine:
    def order_product(self, product_type):
        product = ProductFactory.create_product(product_type)
        if product:
            print("Dispensing:", product.get_name())
        else:
            print("Product not available")


def main():
    vending_machine = VendingMachine()
    while True:
        print("\nSelect product:")
        print("1 - Chocolate")
        print("2 - Chips")
        print("3 - Juice")
        print("0 - Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            vending_machine.order_product("chocolate")
        elif choice == "2":
            vending_machine.order_product("chips")
        elif choice == "3":
            vending_machine.order_product("juice")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
