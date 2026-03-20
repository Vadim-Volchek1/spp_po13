from abc import ABC, abstractmethod
from datetime import datetime


class Book:
    """Книга"""

    def __init__(self, title, author, price, genre):
        self.title = title
        self.author = author
        self.price = price
        self.genre = genre

    def __str__(self):
        return f"'{self.title}' {self.author} - {self.price} руб."


class Account(ABC):
    """Базовый класс учетной записи"""

    def __init__(self, username):
        self.username = username
        self.registration_date = datetime.now()

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_discount(self):
        pass

    @abstractmethod
    def can_access_premium(self):
        pass

    @abstractmethod
    def get_bonus_points(self):
        pass


class BaseAccount(Account):
    """Базовая учетная запись"""

    def __init__(self, username):
        super().__init__(username)
        self.purchases_count = 0
        self.total_spent = 0

    def get_description(self):
        return f"Базовая учетная запись пользователя {self.username}"

    def get_discount(self):
        return 0

    def can_access_premium(self):
        return False

    def get_bonus_points(self):
        return 0

    def add_purchase(self, amount):
        self.purchases_count += 1
        self.total_spent += amount


class AccountDecorator(Account):
    """Базовый декоратор для учетной записи"""

    def __init__(self, account):
        self.account = account
        super().__init__(account.username)

    def get_description(self):
        return self.account.get_description()

    def get_discount(self):
        return self.account.get_discount()

    def can_access_premium(self):
        return self.account.can_access_premium()

    def get_bonus_points(self):
        return self.account.get_bonus_points()

    def add_purchase(self, amount):
        self.account.add_purchase(amount)


class SilverLevel(AccountDecorator):
    """Серебряный уровень (после 5 покупок или 5000 руб.)"""

    def get_description(self):
        return f"{self.account.get_description()} + Серебряный уровень"

    def get_discount(self):
        return 5  # 5% скидка

    def can_access_premium(self):
        return True

    def get_bonus_points(self):
        return 10  # 10 бонусов за покупку

    def get_special_offers(self):
        return ["Скидка 5% на весь ассортимент", "Бесплатная доставка при заказе от 1000 руб."]


class GoldLevel(AccountDecorator):
    """Золотой уровень (после 15 покупок или 15000 руб.)"""

    def get_description(self):
        return f"{self.account.get_description()} + Золотой уровень"

    def get_discount(self):
        return 10  # 10% скидка

    def can_access_premium(self):
        return True

    def get_bonus_points(self):
        return 25  # 25 бонусов за покупку

    def get_special_offers(self):
        return [
            "Скидка 10% на весь ассортимент",
            "Бесплатная доставка",
            "Ранний доступ к новинкам",
            "Подарок при заказе от 2000 руб.",
        ]


class PlatinumLevel(AccountDecorator):
    """Платиновый уровень (после 30 покупок или 30000 руб.)"""

    def get_description(self):
        return f"{self.account.get_description()} + Платиновый уровень"

    def get_discount(self):
        return 15  # 15% скидка

    def can_access_premium(self):
        return True

    def get_bonus_points(self):
        return 50  # 50 бонусов за покупку

    def get_special_offers(self):
        return [
            "Скидка 15% на весь ассортимент",
            "Бесплатная доставка",
            "Эксклюзивные издания",
            "Личный менеджер",
            "Подарок при каждом заказе",
            "Участие в закрытых распродажах",
        ]


class VIPLevel(AccountDecorator):
    """VIP уровень (после 50 покупок или 50000 руб.)"""

    def get_description(self):
        return f"{self.account.get_description()} + VIP уровень"

    def get_discount(self):
        return 20  # 20% скидка

    def can_access_premium(self):
        return True

    def get_bonus_points(self):
        return 100  # 100 бонусов за покупку

    def get_special_offers(self):
        return [
            "Скидка 20% на весь ассортимент",
            "Бесплатная доставка в любой город",
            "Эксклюзивные издания с автографом",
            "Личный менеджер 24/7",
            "Подарок к каждому заказу",
            "Приоритетное обслуживание",
            "Доступ к аукционам редких книг",
        ]


class BookStore:
    """Книжный интернет-магазин"""

    def __init__(self, name):
        self.name = name
        self.books = []
        self.accounts = {}

    def add_book(self, book):
        self.books.append(book)

    def register_user(self, username):
        account = BaseAccount(username)
        self.accounts[username] = account
        print(f"Зарегистрирован новый пользователь: {username}")
        return account

    def get_account(self, username):
        return self.accounts.get(username)

    def update_account_level(self, username):
        """Обновляет уровень учетной записи на основе активности"""
        account = self.get_account(username)
        if not account:
            return None

        # Получаем базовый аккаунт (без декораторов)
        while hasattr(account, "account"):
            account = account.account

        # Проверяем уровень активности
        if account.total_spent >= 50000 or account.purchases_count >= 50:
            return VIPLevel(account)
        if account.total_spent >= 30000 or account.purchases_count >= 30:
            return PlatinumLevel(account)
        if account.total_spent >= 15000 or account.purchases_count >= 15:
            return GoldLevel(account)
        if account.total_spent >= 5000 or account.purchases_count >= 5:
            return SilverLevel(account)
        return account

    def make_purchase(self, username, book_indices):
        """Совершение покупки"""
        account = self.get_account(username)
        if not account:
            print(f"Пользователь {username} не найден")
            return None

        total = 0
        purchased_books = []

        print(f"\n--- ПОКУПКА ДЛЯ {username} ---")

        for idx in book_indices:
            if 0 <= idx < len(self.books):
                book = self.books[idx]
                price_with_discount = book.price * (1 - account.get_discount() / 100)
                total += price_with_discount
                purchased_books.append((book, price_with_discount))
                print(f"  {book.title} - {book.price} руб. -> "
      f"со скидкой {price_with_discount:.0f} руб.")

        # Добавляем покупку в историю
        base_account = account
        while hasattr(base_account, "account"):
            base_account = base_account.account
        base_account.add_purchase(total)

        # Начисляем бонусы
        bonus = account.get_bonus_points() * len(book_indices)
        print(f"  Начислено бонусов: {bonus}")
        print(f"  Итого к оплате: {total:.0f} руб.")

        # Обновляем уровень
        self.accounts[username] = self.update_account_level(username)
        print(f"  Текущий уровень: {self.accounts[username].get_description()}")

        return total


def demo():  # pylint: disable=too-many-locals, too-many-statements
    """Демонстрация работы книжного магазина"""
    print("=" * 70)
    print("КНИЖНЫЙ ИНТЕРНЕТ-МАГАЗИН (ПАТТЕРН: ДЕКОРАТОР)")
    print("=" * 70)

    # Создаем магазин
    store = BookStore("Читай-город")

    # Добавляем книги
    print("\n--- АССОРТИМЕНТ ---")
    books = [
        Book("Война и мир", "Л. Толстой", 1200, "роман"),
        Book("Преступление и наказание", "Ф. Достоевский", 800, "роман"),
        Book("Мастер и Маргарита", "М. Булгаков", 950, "роман"),
        Book("1984", "Д. Оруэлл", 700, "антиутопия"),
        Book("Маленький принц", "А. Сент-Экзюпери", 500, "сказка"),
        Book("Три товарища", "Э.М. Ремарк", 850, "роман"),
        Book("Портрет Дориана Грея", "О. Уайльд", 650, "роман"),
        Book("Гарри Поттер", "Дж. Роулинг", 1500, "фэнтези"),
    ]

    for book in books:
        store.add_book(book)
        print(f"  {book}")

    # Регистрируем пользователей
    print("\n--- РЕГИСТРАЦИЯ ---")
    users = ["ivan", "maria", "alexey", "elena"]
    for user in users:
        store.register_user(user)

    # Демонстрация 1: Иван только начал
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ 1: Новый пользователь (базовый уровень)")
    print("=" * 70)

    ivan_account = store.get_account("ivan")
    print(f"Описание: {ivan_account.get_description()}")
    print(f"Скидка: {ivan_account.get_discount()}%")
    print(f"Доступ к премиум: {ivan_account.can_access_premium()}")
    print(f"Бонусы за покупку: {ivan_account.get_bonus_points()}")

    # Первая покупка
    store.make_purchase("ivan", [0, 3])  # Война и мир + 1984

    # Демонстрация 2: Мария достигает серебряного уровня
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ 2: Достижение серебряного уровня")
    print("=" * 70)

    # Мария делает несколько покупок
    store.make_purchase("maria", [1, 2])  # Преступление и наказание + Мастер и Маргарита
    store.make_purchase("maria", [4, 5])  # Маленький принц + Три товарища
    store.make_purchase("maria", [6])  # Портрет Дориана Грея

    maria_account = store.get_account("maria")
    print(f"\nИтоговый уровень Марии: {maria_account.get_description()}")
    print(f"Скидка: {maria_account.get_discount()}%")
    print(f"Доступ к премиум: {maria_account.can_access_premium()}")

    # Показываем специальные предложения для серебряного уровня
    if hasattr(maria_account, "get_special_offers"):
        print("Специальные предложения:")
        for offer in maria_account.get_special_offers():
            print(f"  • {offer}")

    # Демонстрация 3: Алексей достигает золотого уровня
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ 3: Достижение золотого уровня")
    print("=" * 70)

    # Алексей делает много покупок
    for _ in range(8):
        store.make_purchase("alexey", [0, 1, 2, 3, 4])

    alexey_account = store.get_account("alexey")
    print(f"\nИтоговый уровень Алексея: {alexey_account.get_description()}")
    print(f"Скидка: {alexey_account.get_discount()}%")

    if hasattr(alexey_account, "get_special_offers"):
        print("Специальные предложения:")
        for offer in alexey_account.get_special_offers():
            print(f"  • {offer}")

    # Демонстрация 4: Сравнение всех уровней
    print("\n" + "=" * 70)
    print("СРАВНЕНИЕ УРОВНЕЙ УЧЕТНЫХ ЗАПИСЕЙ")
    print("=" * 70)

    # Создаем все уровни для демонстрации
    base = BaseAccount("demo")
    silver = SilverLevel(base)
    gold = GoldLevel(silver)
    platinum = PlatinumLevel(gold)
    vip = VIPLevel(platinum)

    levels = [
        ("Базовый", base),
        ("Серебряный", silver),
        ("Золотой", gold),
        ("Платиновый", platinum),
        ("VIP", vip)
    ]

    for level_name, level in levels:
        print(f"\n{level_name} уровень:")
        print(f"  Описание: {level.get_description()}")
        print(f"  Скидка: {level.get_discount()}%")
        print(f"  Бонусы: {level.get_bonus_points()}")
        if hasattr(level, "get_special_offers"):
            offers = level.get_special_offers()
            print(f"  Предложений: {len(offers)}")
            if level_name == "VIP":
                print(f"  Топ-предложение: {offers[0]}")


if __name__ == "__main__":
    demo()
