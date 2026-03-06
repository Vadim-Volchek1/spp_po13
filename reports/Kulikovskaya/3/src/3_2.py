from abc import ABC, abstractmethod
from dataclasses import dataclass


# Целевой интерфейс (Target) - цифровые часы

class DigitalClockInterface(ABC):

    @abstractmethod
    def get_time(self) -> str:
        pass

    @abstractmethod
    def set_time(self, hours: int, minutes: int, seconds: int) -> None:
        pass

    @abstractmethod
    def display(self) -> str:
        pass


# Адаптируемый класс (Adaptee) - аналоговые часы

@dataclass
class AnalogClockState:
    """Состояние аналоговых часов (угол поворота стрелок)"""
    hour_angle: float  # угол часовой стрелки (0-360)
    minute_angle: float  # угол минутной стрелки (0-360)
    second_angle: float  # угол секундной стрелки (0-360)


class AnalogClock:
    def __init__(self):
        self._state = AnalogClockState(0.0, 0.0, 0.0)
        self._min_angle = 0.0  # минимальный угол
        self._max_angle = 360.0  # максимальный угол

    def set_hands(self, hour_angle: float, minute_angle: float, second_angle: float) -> None:
        """Установить положение стрелок по углам"""
        # Нормализация углов (0-360)
        self._state.hour_angle = hour_angle % 360
        self._state.minute_angle = minute_angle % 360
        self._state.second_angle = second_angle % 360

    def get_hands_position(self) -> AnalogClockState:
        """Получить текущее положение стрелок"""
        return self._state

    def move_hands(self, hour_delta: float, minute_delta: float, second_delta: float) -> None:
        """Повернуть стрелки на заданный угол"""
        self._state.hour_angle = (self._state.hour_angle + hour_delta) % 360
        self._state.minute_angle = (self._state.minute_angle + minute_delta) % 360
        self._state.second_angle = (self._state.second_angle + second_delta) % 360

    def display_analog(self) -> str:
        """Отобразить аналоговые часы в текстовом виде"""
        return (
            f"   Аналоговые часы:\n"
            f"   Часовая стрелка:   {self._state.hour_angle:6.1f}°\n"
            f"   Минутная стрелка:  {self._state.minute_angle:6.1f}°\n"
            f"   Секундная стрелка: {self._state.second_angle:6.1f}°"
        )

    def get_limits(self) -> tuple:
        """Получить границы измерений"""
        return (self._min_angle, self._max_angle)


# Адаптер (Adapter) - адаптирует аналоговые часы под цифровой интерфейс

class AnalogToDigitalAdapter(DigitalClockInterface):
    def __init__(self, analog_clock: AnalogClock):
        self._analog_clock = analog_clock

    def _angles_to_time(self, state: AnalogClockState) -> tuple:
        """Конвертация углов стрелок в время"""
        # Часовая стрелка: 360° = 12 часов = 30° за час
        hours = int(state.hour_angle / 30) % 12
        if hours == 0:
            hours = 12

        # Минутная стрелка: 360° = 60 минут = 6° за минуту
        minutes = int(state.minute_angle / 6) % 60

        # Секундная стрелка: 360° = 60 секунд = 6° за секунду
        seconds = int(state.second_angle / 6) % 60

        return (hours, minutes, seconds)

    def _time_to_angles(self, hours: int, minutes: int, seconds: int) -> AnalogClockState:
        """Конвертация времени в углы стрелок"""
        # Часовая стрелка учитывает минуты для плавности
        hour_angle = (hours % 12) * 30 + (minutes / 60) * 30
        minute_angle = minutes * 6 + (seconds / 60) * 6
        second_angle = seconds * 6

        return AnalogClockState(hour_angle, minute_angle, second_angle)

    def get_time(self) -> str:
        """Получить время в цифровом формате"""
        state = self._analog_clock.get_hands_position()
        hours, minutes, seconds = self._angles_to_time(state)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def set_time(self, hours: int, minutes: int, seconds: int) -> None:
        """Установить время (конвертируется в углы)"""
        # Валидация
        if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
            raise ValueError("Некорректное время")

        state = self._time_to_angles(hours, minutes, seconds)
        self._analog_clock.set_hands(state.hour_angle, state.minute_angle, state.second_angle)

    def display(self) -> str:
        """Отобразить время в цифровом формате"""
        time_str = self.get_time()
        return (
            f"Цифровой дисплей:\n"
            f"   {time_str} \n"
        )

    def get_detailed_info(self) -> str:
        """Получить детальную информацию (и аналог, и цифра)"""
        analog_display = self._analog_clock.display_analog()
        digital_display = self.display()
        return f"{analog_display}\n{digital_display}"


# Дополнительный адаптер для обратной совместимости

class DigitalToAnalogAdapter:
    def __init__(self, digital_clock: DigitalClockInterface):
        self._digital_clock = digital_clock

    def get_hands_position(self) -> AnalogClockState:
        """Получить положение стрелок из цифрового времени"""
        time_str = self._digital_clock.get_time()
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])

        # Конвертация в углы
        hour_angle = (hours % 12) * 30 + (minutes / 60) * 30
        minute_angle = minutes * 6 + (seconds / 60) * 6
        second_angle = seconds * 6

        return AnalogClockState(hour_angle, minute_angle, second_angle)


# Клиентский код

class ClockUser:
    def __init__(self, clock: DigitalClockInterface):
        self._clock = clock

    def check_time(self) -> str:
        """Проверить время"""
        return self._clock.get_time()

    def set_alarm(self, hours: int, minutes: int) -> str:
        """Установить будильник (демонстрация работы с интерфейсом)"""
        # Для демонстрации просто сохраняем время
        return f"Будильник установлен на {hours:02d}:{minutes:02d}"

    def show_clock(self) -> str:
        """Показать часы"""
        return self._clock.display()


# Реальные цифровые часы (для сравнения)

class RealDigitalClock(DigitalClockInterface):
    def __init__(self):
        self._hours = 0
        self._minutes = 0
        self._seconds = 0

    def get_time(self) -> str:
        return f"{self._hours:02d}:{self._minutes:02d}:{self._seconds:02d}"

    def set_time(self, hours: int, minutes: int, seconds: int) -> None:
        self._hours = hours % 24
        self._minutes = minutes % 60
        self._seconds = seconds % 60

    def display(self) -> str:
        return f"[DIGITAL] {self.get_time()}"


# Демонстрация работы
if __name__ == "__main__":
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА 'АДАПТЕР'")
    print("Адаптация аналоговых часов под цифровой интерфейс")

    # 1. Создание аналоговых часов
    print("\n1. Создание аналоговых часов")
    analog = AnalogClock()

    # Установка времени через углы стрелок (как это делается на аналоговых часах)
    # 10:30:45 -> часовая: 315°, минутная: 183°, секундная: 270°
    analog.set_hands(315, 183, 270)
    print(analog.display_analog())

    # 2. Использование адаптера
    print("\n2. Подключение адаптера (Analog -> Digital)")
    adapter = AnalogToDigitalAdapter(analog)
    print(f"Цифровое время: {adapter.get_time()}")
    print(adapter.display())

    # 3. Клиентский код работает с адаптированными часами
    print("\n3. Работа клиентского кода через единый интерфейс")
    user = ClockUser(adapter)
    print(f"Пользователь видит время: {user.check_time()}")
    print(user.set_alarm(7, 0))
    print(user.show_clock())

    # 4. Установка времени через цифровой интерфейс
    print("\n4. Установка времени через цифровой интерфейс")
    print("Устанавливаем время 14:45:30 через адаптер...")
    adapter.set_time(14, 45, 30)
    print(adapter.get_detailed_info())

    # 5. Сравнение с реальными цифровыми часами
    print("\n5. Сравнение с реальными цифровыми часами")
    real_digital = RealDigitalClock()
    real_digital.set_time(14, 45, 30)

    print("Реальные цифровые часы:")
    print(real_digital.display())

    print("\nАдаптированные аналоговые часы:")
    print(adapter.display())

    print(f"\nВремя совпадает: {real_digital.get_time() == adapter.get_time()}")

    # 6. Демонстрация движения стрелок
    print("\n6. Демонстрация движения времени")
    print("Начальное время:", adapter.get_time())

    # Симуляция движения времени (поворот стрелок)
    for i in range(3):
        analog.move_hands(0.5, 6, 6)  # часы +0.5°, минуты +6°, секунды +6°
        print(f"После движения стрелок: {adapter.get_time()}")

    print("Демонстрация завершена!")
    print("Паттерн Адаптер позволил использовать аналоговые часы")
    print("через цифровой интерфейс без изменения их кода.")
