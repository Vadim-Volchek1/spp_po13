class DigitalClock:

    def get_hours(self):
        pass

    def get_minutes(self):
        pass

    def get_time(self):
        pass


class AnalogClock:

    def __init__(self, hour_angle, minute_angle):
        # угол часовой стрелки от 12 часов (0-360)
        self.hour_angle = hour_angle % 360
        # угол минутной стрелки от 12 часов (0-360)
        self.minute_angle = minute_angle % 360

    def set_by_time(self, hours, minutes):
        # минутная: 360 гр / 60 = 6 гр на минуту
        self.minute_angle = (minutes * 6) % 360
        # часовая: 30 гр на час + 0.5 гр на минуту
        self.hour_angle = ((hours % 12) * 30 + minutes * 0.5) % 360

    def get_hour_angle(self):
        return self.hour_angle

    def get_minute_angle(self):
        return self.minute_angle


# адаптер
class ClockAdapter(DigitalClock):

    def __init__(self, analog_clock):
        self.analog_clock = analog_clock

    def get_hours(self):
        # 360 гр = 12 часов, значит 1 час = 30 гр
        hours = (self.analog_clock.get_hour_angle() / 30) % 12
        return int(hours)

    def get_minutes(self):
        # 360 гр = 60 минут, значит 1 минута = 6 гр
        minutes = (self.analog_clock.get_minute_angle() / 6) % 60
        return int(minutes)

    def get_time(self):
        hours = self.get_hours()
        minutes = self.get_minutes()
        return f"{hours:02d}:{minutes:02d}"


def main():
    print("=" * 50)
    print("ПРОЕКТ «ЧАСЫ» — ПАТТЕРН АДАПТЕР")
    print("=" * 50)

    # создаём аналоговые часы (хранят углы)
    analog = AnalogClock(90, 180)  # часовая на 90 гр (3ч) а минутная на 180 гр (30 мин)
    print(f"Аналоговые часы: hour_angle={analog.hour_angle}°, minute_angle={analog.minute_angle}°")

    # оборачиваем в адаптер
    adapter = ClockAdapter(analog)

    print("\nЧерез адаптер:")
    print(f"  Часы:   {adapter.get_hours()} ч")
    print(f"  Минуты: {adapter.get_minutes()} мин")
    print(f"  Время:  {adapter.get_time()}")

    print("\n" + "-" * 50)
    print("Устанавливаем время 14:45 (2:45) через аналоговые часы:")
    analog.set_by_time(14, 45)
    print(f"  Углы: часовая={analog.hour_angle}°, минутная={analog.minute_angle}°")
    print(f"  Через адаптер: {adapter.get_time()}")

    print("\n" + "-" * 50)
    print("Демонстрация разных углов:")

    test_angles = [
        (0, 0),  # 12:00
        (90, 0),  # 3:00
        (180, 180),  # 6:30
        (270, 330),  # 9:55
    ]

    for hour_angle, minute_angle in test_angles:
        analog = AnalogClock(hour_angle, minute_angle)
        adapter = ClockAdapter(analog)
        print(f"  Углы ({hour_angle:3.0f}°, {minute_angle:3.0f}°) -> время {adapter.get_time()}")


if __name__ == "__main__":
    main()
