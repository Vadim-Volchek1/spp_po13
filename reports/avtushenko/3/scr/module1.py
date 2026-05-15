from abc import ABC, abstractmethod


# Целевой интерфейс (цифровые часы)
class DigitalClock(ABC):
    @abstractmethod
    def get_time(self) -> str:
        pass


# Адаптируемый класс (часы со стрелками)
class AnalogClock:
    def __init__(self, hours: int = 0, minutes: int = 0):
        self.hours = hours % 12
        self.minutes = minutes % 60

    def get_hours_angle(self) -> float:
        return self.hours * 30 + self.minutes * 0.5

    def get_minutes_angle(self) -> float:
        return self.minutes * 6

    def set_time(self, hours: int, minutes: int):
        self.hours = hours % 12
        self.minutes = minutes % 60

    def __str__(self):
        return f"Стрелки: часы={self.get_hours_angle():.1f}°, минуты={self.get_minutes_angle():.1f}°"


# Адаптер (часы со стрелками -> цифровые)
class AnalogToDigitalAdapter(DigitalClock):
    def __init__(self, analog_clock: AnalogClock):
        self._clock = analog_clock

    def get_time(self) -> str:
        h, m = self._clock.hours, self._clock.minutes
        return f"{h:02d}:{m:02d}"

    def set_time(self, hours: int, minutes: int):
        self._clock.set_time(hours, minutes)

    def __str__(self):
        return f"Цифровые: {self.get_time()} | {self._clock}"


# Демонстрация
if __name__ == "__main__":
    # Часы со стрелками
    analog = AnalogClock(3, 45)
    print("Только аналоговые:")
    print(f"  {analog}")

    # Адаптер для использования как цифровых
    adapter = AnalogToDigitalAdapter(analog)
    print("\nЧерез адаптер:")
    print(f"  {adapter}")
    print(f"  Время: {adapter.get_time()}")

    # Изменение времени
    print("\nУстановка 10:30:")
    adapter.set_time(10, 30)
    print(f"  {adapter}")

    print("\nУстановка 0:15:")
    adapter.set_time(0, 15)
    print(f"  {adapter}")
