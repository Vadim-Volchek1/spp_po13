class Book:
    def __init__(self, title, author, year, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn
        self.is_available = True
        self.location = "каталог"

    def __str__(self):
        status = "в наличии" if self.is_available else "недоступна"
        return f"'{self.title}', {self.author} ({self.year}) - {status}"

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False


class Catalog:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        if book not in self.books:
            self.books.append(book)
            print(f"Книга {book.title} добавлена в каталог")
        else:
            print("Такая книга уже есть в каталоге")

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            print(f"Книга {book.title} удалена из каталога")

    def search_by_title(self, title):
        result = []
        for book in self.books:
            if title.lower() in book.title.lower():
                result.append(book)
        return result

    def search_by_author(self, author):
        result = []
        for book in self.books:
            if author.lower() in book.author.lower():
                result.append(book)
        return result

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def show_all_books(self):
        print("Каталог: ")
        if not self.books:
            print("<пусто>")
        else:
            for i, book in enumerate(self.books, 1):
                print(f"{i}. {book}")


class Reader:
    def __init__(self, name, reader_id):
        self.name = name
        self.reader_id = reader_id
        self.orders = []
        self.borrowed_books = []
        self.is_blacklisted = False

    def __str__(self):
        status = " (В ЧЕРНОМ СПИСКЕ)" if self.is_blacklisted else ""
        return f"Читатель: {self.name} (ID: {self.reader_id}){status}"

    def create_order(self, book, order_type):
        if self.is_blacklisted:
            print(f"{self.name} в черном списке! Заказ невозможен")
            return None

        order = Order(self, book, order_type)
        self.orders.append(order)
        print(f"Заказ оформлен: {self.name} -> {book.title} ({order_type})")
        return order

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.is_available = True
            book.location = "каталог"
            print(f"{self.name} вернул книгу '{book.title}'")
            return True
        print(f"У {self.name} нет такой книги")
        return False

    def show_borrowed_books(self):
        if not self.borrowed_books:
            print(f"{self.name} не взял ни одной книги")
        else:
            print(f"Книги у {self.name}:")
            for book in self.borrowed_books:
                print(f"  - {book}")


class Order:
    def __init__(self, reader, book, order_type):
        self.reader = reader
        self.book = book
        self.order_type = order_type
        self.is_completed = False
        self.is_cancelled = False

    def __str__(self):
        status = "выполнен" if self.is_completed else "отменен" if self.is_cancelled else "активен"
        return f"Заказ: {self.reader.name} -> {self.book.title} ({self.order_type}) - {status}"


class Librarian:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id
        self.issued_books = []

    def __str__(self):
        return f"Библиотекарь: {self.name} (ID: {self.employee_id})"

    def process_order(self, order):
        if order.is_completed or order.is_cancelled:
            print("Заказ уже обработан")
            return False

        book = order.book

        if not book.is_available:
            print(f"Книга '{book.title}' недоступна")
            order.is_cancelled = True
            return False

        if order.reader.is_blacklisted:
            print(f"Читатель {order.reader.name} в черном списке!")
            order.is_cancelled = True
            return False

        book.is_available = False
        book.location = order.order_type
        order.reader.borrowed_books.append(book)
        order.is_completed = True
        self.issued_books.append(book)

        print(f"{self.name} выдал книгу '{book.title}' {order.reader.name} ({order.order_type})")
        return True

    @staticmethod
    def check_return(reader, book):
        return reader.return_book(book)


class Administrator(Librarian):
    def __init__(self, name, employee_id):
        super().__init__(name, employee_id)
        self.blacklist = []

    def __str__(self):
        return f"Администратор: {self.name} (ID: {self.employee_id})"

    def add_to_blacklist(self, reader, reason=""):
        if reader not in self.blacklist:
            reader.is_blacklisted = True
            self.blacklist.append(reader)
            reason_text = f"по причине: {reason}" if reason else "<не указано>"
            print(f"{self.name} занес {reader.name} в черный список {reason_text}")
        else:
            print(f"{reader.name} уже в черном списке")

    def remove_from_blacklist(self, reader):
        if reader in self.blacklist:
            reader.is_blacklisted = False
            self.blacklist.remove(reader)
            print(f"{self.name} удалил {reader.name} из черного списка")
        else:
            print(f"{reader.name} не найден в черном списке")

    def show_blacklist(self):
        print("ЧЕРНЫЙ СПИСОК:")
        if not self.blacklist:
            print("<пусто>")
        else:
            for reader in self.blacklist:
                print(f"  - {reader.name} (ID: {reader.reader_id})")


print("СИСТЕМА БИБЛИОТЕКА")
catalog = Catalog()

book1 = Book("Война и мир", "Лев Толстой", 1869, "978-5-699-38289-1")
book2 = Book("Преступление и наказание", "Федор Достоевский", 1866, "978-5-17-123456-7")
book3 = Book("Анна Каренина", "Лев Толстой", 1877, "978-5-699-38290-7")
book4 = Book("Мастер и Маргарита", "Михаил Булгаков", 1967, "978-5-389-12345-6")

print("\nДобавление книг в каталог")
catalog.add_book(book1)
catalog.add_book(book2)
catalog.add_book(book3)
catalog.add_book(book4)

catalog.show_all_books()

print("\nСоздание сотрудников")
librarian = Librarian("Анна Петровна", "LIB001")
admin = Administrator("Иван Иванович", "ADM001")

print(librarian)
print(admin)

print("\nСоздание читателей ")
reader1 = Reader("Петр Сидоров", "R001")
reader2 = Reader("Мария Иванова", "R002")
reader3 = Reader("Алексей Смирнов", "R003")

print(reader1)
print(reader2)
print(reader3)

print("\nПоиск книг по автору 'Толстой' ")
tolstoy_books = catalog.search_by_author("Толстой")
for tolstoy_book in tolstoy_books:
    print(f"Найдено: {tolstoy_book}")

print("\nОформление заказов ")
order1 = reader1.create_order(book1, "абонемент")
order2 = reader2.create_order(book2, "читальный зал")
order3 = reader3.create_order(book4, "абонемент")

print("\nОбработка заказов библиотекарем ")
librarian.process_order(order1)
librarian.process_order(order2)

print("\nПопытка заказать уже выданную книгу ")
order_again = reader3.create_order(book1, "абонемент")
librarian.process_order(order_again)

print("\nВозврат книги ")
reader1.show_borrowed_books()
librarian.check_return(reader1, book1)
reader1.show_borrowed_books()

print("\nЗаказ вернувшейся книги ")
order_new = reader3.create_order(book1, "абонемент")
librarian.process_order(order_new)

print("\nРабота с черным списком ")
print(reader2)
admin.add_to_blacklist(reader2, "не вернул книгу вовремя")
admin.show_blacklist()
print(reader2)

print("\nПопытка заказа книгу читателем из ЧС ")
bad_order = reader2.create_order(book3, "читальный зал")
if bad_order:
    librarian.process_order(bad_order)

print("\nУдаление из черного списка ")
admin.remove_from_blacklist(reader2)
admin.show_blacklist()
print(reader2)

print("\nИтоговое состояние ")
catalog.show_all_books()
reader1.show_borrowed_books()
reader2.show_borrowed_books()
reader3.show_borrowed_books()
