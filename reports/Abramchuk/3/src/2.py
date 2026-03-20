# Adapter (Адаптер)

from abc import ABC, abstractmethod


class IDigitalClock(ABC):
    @abstractmethod
    def get_time(self) -> str:
        pass


class DigitalClock(IDigitalClock):
    def __init__(self, time):
        self.time = time

    def get_time(self) -> str:
        return self.time


class ClockWithHands:
    def __init__(self, hour_angle, minute_angle):
        self.hour_angle = hour_angle
        self.minute_angle = minute_angle

    def get_time_angles(self) -> str:
        return f"{self.hour_angle}, {self.minute_angle}"


class ClockAdapter(IDigitalClock):
    def __init__(self, clock_with_hands: ClockWithHands):
        self.clock_with_hands = clock_with_hands

    def get_time(self):
        h = int(self.clock_with_hands.hour_angle / 30)
        m = int(self.clock_with_hands.minute_angle / 6)

        return f"{h:02d}:{m:02d}"


analog = ClockWithHands(120, 180)
adapter = ClockAdapter(analog)

print(adapter.get_time())
