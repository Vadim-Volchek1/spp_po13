import random


class ElectronicThermometer:
    def __init__(self, name):
        self.name = name
        self.is_on = False
        self.current_temperature = 0.0

    def __str__(self):
        status = "включен" if self.is_on else "выключен"
        return f"Электронный градусник '{self.name}': {self.current_temperature}°C ({status})"

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            print(f"Электронный градусник '{self.name}' включен")
        else:
            print(f"Электронный градусник '{self.name}' уже включен")

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            print(f"Электронный градусник '{self.name}' выключен")
        else:
            print(f"Электронный градусник '{self.name}' уже выключен")

    def measure_temperature(self):
        if not self.is_on:
            print(f"Ошибка: градусник '{self.name}' выключен!")
            return None

        self.current_temperature = round(random.uniform(35.0, 42.0), 1)
        return self.current_temperature

    def get_temperature(self):
        return self.current_temperature if self.is_on else None


class AnalogThermometer:
    def __init__(self, name, min_temp, max_temp, max_height_mm=100):
        self.name = name
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.max_height_mm = max_height_mm
        self.mercury_height = 0.0

    def __str__(self):
        return (f"Аналоговый градусник '{self.name}': "
                f"диапазон [{self.min_temp}°C, {self.max_temp}°C], "
                f"столб {self.mercury_height}мм")

    def shake(self):
        self.mercury_height = 0
        print(f"Аналоговый градусник '{self.name}' встряхнут")

    def measure_with_mercury(self, temperature_celsius):
        if temperature_celsius < self.min_temp or temperature_celsius > self.max_temp:
            print(f"Температура {temperature_celsius}°C вне диапазона измерений!")
            return False

        self.mercury_height = round(((temperature_celsius - self.min_temp) / (
                self.max_temp - self.min_temp)) * self.max_height_mm, 1)

        print(f"Аналоговый градусник '{self.name}' измерил: "
              f"столб поднялся на {self.mercury_height:.1f}мм")
        return True

    def get_mercury_height(self):
        return self.mercury_height


class ThermometerAdapter(ElectronicThermometer):
    def __init__(self, analog_thermometer):
        super().__init__(f"Адаптер для {analog_thermometer.name}")

        self.analog = analog_thermometer
        self.last_measured_temp = 0.0

    def __str__(self):
        return (f"Адаптер: {self.analog.name} -> {self.name}\n"
                f"Состояние: {'включен' if self.is_on else 'выключен'}\n"
                f"Текущие показания: {self.last_measured_temp}°C")

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            print(f"Адаптер для '{self.analog.name}' активирован")
        else:
            print(f"Адаптер для '{self.analog.name}' уже активирован")

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            print(f"Адаптер для '{self.analog.name}' деактивирован")
        else:
            print(f"Адаптер для '{self.analog.name}' уже деактивирован")

    def measure_temperature(self):
        if not self.is_on:
            print(f"Ошибка: адаптер для '{self.analog.name}' выключен!")
            return None

        self.analog.shake()

        temp_to_measure = round(random.uniform(
            self.analog.min_temp + 1,
            self.analog.max_temp - 1
        ), 1)

        success = self.analog.measure_with_mercury(temp_to_measure)

        if success:
            temp_range = self.analog.max_temp - self.analog.min_temp
            height_range = self.analog.max_height_mm
            mercury_height = self.analog.get_mercury_height()

            self.last_measured_temp = round(
                (mercury_height / height_range) * temp_range + self.analog.min_temp,
                1
            )

            print(f"Адаптер преобразовал: {mercury_height:.1f}мм -> {self.last_measured_temp}°C")
            return self.last_measured_temp
        print("Не удалось измерить температуру...")
        return None

    def get_temperature(self):
        return self.last_measured_temp if self.is_on else None


class MedicalCabinet:
    def __init__(self, name):
        self.name = name
        self.thermometers = []

    def __str__(self):
        return f"Медицинский кабинет '{self.name}' (градусников: {len(self.thermometers)})"

    def add_thermometer(self, thermometer):
        self.thermometers.append(thermometer)
        print(f"В кабинет добавлен: {thermometer.name}")

    def measure_patient(self, patient_name):
        print(f"\nИзмерение температуры пациента '{patient_name}':")

        results = {}
        for thermo in self.thermometers:
            print(f"\nИспользуем: {thermo.name}")

            if hasattr(thermo, 'turn_on'):
                thermo.turn_on()

            temperature = thermo.measure_temperature()
            if temperature is not None:
                results[thermo.name] = temperature
                print(f"Результат: {temperature}°C")
            else:
                print(f"Не удалось измерить температуру...")

            if hasattr(thermo, 'turn_off'):
                thermo.turn_off()

        return results


print("Создание градусников:")

electronic = ElectronicThermometer("Eco Thermometer")
print(electronic)

analog = AnalogThermometer("Ртутный", min_temp=34, max_temp=42, max_height_mm=120)
print(analog)

adapter = ThermometerAdapter(analog)
print(adapter)

print("\nСоздание медицинского кабинета:")
cabinet = MedicalCabinet("Кабинет 142")
print(cabinet)
cabinet.add_thermometer(electronic)
cabinet.add_thermometer(adapter)

print(cabinet.measure_patient("Пациент 1"))

print(f"\nИсходный {analog}")
analog.measure_with_mercury(38.5)
print(f"После измерения: {analog}")
print(f"Высота столба: {analog.get_mercury_height():.1f}мм")

adapter.turn_on()
temp = adapter.measure_temperature()
if temp:
    print(f"Получена температура: {temp}°C")
print(f"\nСостояние аналогового градусника после измерения через адаптер:")
print(analog)
adapter.turn_off()
