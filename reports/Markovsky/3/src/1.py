class Smartphone:
    def __init__(self, model, screen_size, ram, storage, camera_mp, battery):
        self.model = model
        self.screen_size = screen_size
        self.ram = ram
        self.storage = storage
        self.camera_mp = camera_mp
        self.battery = battery
        self.is_on = False

    def __str__(self):
        status = "включен" if self.is_on else "выключен"
        return (f"{self.model}: экран {self.screen_size}\", {self.ram}ГБ ОЗУ, "
                f"{self.storage}ГБ память, камера {self.camera_mp}МП, "
                f"батарея {self.battery}мАч ({status})")

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            print(f"{self.model} включен")
        else:
            print(f"{self.model} уже включен")

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            print(f"{self.model} выключен")
        else:
            print(f"{self.model} уже выключен")


class SmartphoneFactory:
    def create_smartphone(self):
        pass


class SamsungGalaxyFactory(SmartphoneFactory):
    def create_smartphone(self):
        return Smartphone(
            model="Samsung Galaxy S23",
            screen_size=6.1,
            ram=8,
            storage=256,
            camera_mp=50,
            battery=3900
        )


class IPhoneFactory(SmartphoneFactory):
    def create_smartphone(self):
        return Smartphone(
            model="iPhone 15 Pro",
            screen_size=6.1,
            ram=6,
            storage=256,
            camera_mp=48,
            battery=3274
        )


class XiaomiFactory(SmartphoneFactory):
    def create_smartphone(self):
        return Smartphone(
            model="Xiaomi 13 Pro",
            screen_size=6.73,
            ram=12,
            storage=512,
            camera_mp=50,
            battery=4820
        )


class GooglePixelFactory(SmartphoneFactory):
    def create_smartphone(self):
        return Smartphone(
            model="Google Pixel 8 Pro",
            screen_size=6.7,
            ram=12,
            storage=128,
            camera_mp=50,
            battery=5050
        )


class OnePlusFactory(SmartphoneFactory):
    def create_smartphone(self):
        return Smartphone(
            model="OnePlus 11",
            screen_size=6.7,
            ram=16,
            storage=256,
            camera_mp=50,
            battery=5000
        )


class SmartphonePlant:
    def __init__(self, name):
        self.name = name
        self.produced_phones = []
        self.factories = {
            "samsung": SamsungGalaxyFactory(),
            "iphone": IPhoneFactory(),
            "xiaomi": XiaomiFactory(),
            "google": GooglePixelFactory(),
            "oneplus": OnePlusFactory()
        }

    def __str__(self):
        return f"Завод '{self.name}' (произведено смартфонов: {len(self.produced_phones)})"

    def produce_smartphone(self, model_key):
        if model_key.lower() in self.factories:
            factory = self.factories[model_key.lower()]
            phone = factory.create_smartphone()
            self.produced_phones.append(phone)
            print(f"{self.name} произвел: {phone.model}")
            return phone
        print(f"Модель '{model_key}' не производится на заводе")
        return None

    def produce_multiple(self, orders):
        print(f"\nПроизводство '{orders}' на заводе '{self.name}':")
        results = []
        for model_key, count in orders.items():
            for _ in range(count):
                phone = self.produce_smartphone(model_key)
                if phone:
                    results.append(phone)
        return results

    def show_production_stats(self):
        print(f"\nСтатистика '{self.name}':")
        if not self.produced_phones:
            print("Завод еще ничего не произвел...")
            return

        stats = {}
        for phone in self.produced_phones:
            stats[phone.model] = stats.get(phone.model, 0) + 1

        print(f"Всего произведено: {len(self.produced_phones)} смартфонов")
        for model, count in stats.items():
            print(f" - {model}: {count} шт.")

    def show_all_phones(self):
        print(f"\nСмартфоны произведённые '{self.name}':")
        if not self.produced_phones:
            print("<пусто>")
        else:
            for i, phone in enumerate(self.produced_phones, 1):
                print(f"{i}. {phone}")


plant = SmartphonePlant("ТехноСмарт")
print(plant)
print()

samsung = plant.produce_smartphone("samsung")
iphone = plant.produce_smartphone("iphone")
xiaomi = plant.produce_smartphone("xiaomi")
print()

plant.produce_smartphone("nokia")
print()

print("Тестирование смартфонов:")
if samsung:
    samsung.turn_on()
    samsung.turn_on()
    samsung.turn_off()
print()

if iphone:
    iphone.turn_on()
    iphone.turn_off()
print()

phone_orders = {
    "samsung": 2,
    "iphone": 1,
    "google": 2,
    "oneplus": 1
}
plant.produce_multiple(phone_orders)
print()

plant.show_production_stats()
print()

plant.show_all_phones()
print()

plant2 = SmartphonePlant("ЭкономСмарт")
print(plant2)

print("\nПроизводство на втором заводе:")
plant2.produce_smartphone("xiaomi")
plant2.produce_smartphone("xiaomi")
plant2.produce_smartphone("oneplus")
print()

plant2.show_production_stats()
plant2.show_all_phones()
