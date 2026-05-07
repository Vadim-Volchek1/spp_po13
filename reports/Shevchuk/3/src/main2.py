"""Lab 3, task 2, variant 7.

Structural pattern example: Bridge.
Cars and remote controls are developed independently.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Car(ABC):
    """Abstract car."""

    def __init__(self, model: str) -> None:
        """Initialize a car."""
        if not model.strip():
            raise ValueError("Model cannot be empty.")

        self.model = model
        self.alarm_enabled = False
        self.doors_locked = False
        self.engine_started = False

    @abstractmethod
    def brand(self) -> str:
        """Return car brand."""

    def activate_alarm(self) -> None:
        """Activate alarm."""
        self.alarm_enabled = True
        print(f"{self.brand()} {self.model}: alarm enabled")

    def deactivate_alarm(self) -> None:
        """Deactivate alarm."""
        self.alarm_enabled = False
        print(f"{self.brand()} {self.model}: alarm disabled")

    def lock_doors(self) -> None:
        """Lock doors."""
        self.doors_locked = True
        print(f"{self.brand()} {self.model}: doors locked")

    def unlock_doors(self) -> None:
        """Unlock doors."""
        self.doors_locked = False
        print(f"{self.brand()} {self.model}: doors unlocked")

    def start_engine(self) -> None:
        """Start engine."""
        self.engine_started = True
        print(f"{self.brand()} {self.model}: engine started")

    def stop_engine(self) -> None:
        """Stop engine."""
        self.engine_started = False
        print(f"{self.brand()} {self.model}: engine stopped")

    def show_status(self) -> None:
        """Show current car status."""
        print(
            f"{self.brand()} {self.model}: "
            f"alarm={self.alarm_enabled}, "
            f"locked={self.doors_locked}, "
            f"engine={self.engine_started}"
        )


# pylint: disable=too-few-public-methods
class BMWCar(Car):
    """BMW car."""

    def brand(self) -> str:
        """Return brand."""
        return "BMW"


# pylint: disable=too-few-public-methods
class ToyotaCar(Car):
    """Toyota car."""

    def brand(self) -> str:
        """Return brand."""
        return "Toyota"


# pylint: disable=too-few-public-methods
class AudiCar(Car):
    """Audi car."""

    def brand(self) -> str:
        """Return brand."""
        return "Audi"


class RemoteControl(ABC):
    """Abstract remote control."""

    def __init__(self, car: Car) -> None:
        """Bind remote control to a car."""
        self.car = car

    @abstractmethod
    def toggle_alarm(self) -> None:
        """Toggle alarm mode."""

    @abstractmethod
    def toggle_doors(self) -> None:
        """Toggle doors state."""

    @abstractmethod
    def remote_engine(self) -> None:
        """Start or stop engine remotely."""


class StandardRemote(RemoteControl):
    """Basic remote control."""

    def toggle_alarm(self) -> None:
        """Toggle alarm mode."""
        if self.car.alarm_enabled:
            self.car.deactivate_alarm()
        else:
            self.car.activate_alarm()

    def toggle_doors(self) -> None:
        """Toggle doors state."""
        if self.car.doors_locked:
            self.car.unlock_doors()
        else:
            self.car.lock_doors()

    def remote_engine(self) -> None:
        """Start or stop engine remotely."""
        if self.car.engine_started:
            self.car.stop_engine()
        else:
            self.car.start_engine()


class SecureRemote(RemoteControl):
    """Protected remote control with PIN code."""

    def __init__(self, car: Car, pin_code: str) -> None:
        """Initialize a secure remote."""
        super().__init__(car)
        self.pin_code = pin_code
        self.entered_pin = ""

    def enter_pin(self, pin_attempt: str) -> None:
        """Enter a PIN code."""
        self.entered_pin = pin_attempt

    def toggle_alarm(self) -> None:
        """Toggle alarm mode."""
        print("Secure check completed.")
        if self.car.alarm_enabled:
            self.car.deactivate_alarm()
        else:
            self.car.activate_alarm()

    def toggle_doors(self) -> None:
        """Toggle doors state."""
        print("Protected doors control is active.")
        if self.car.doors_locked:
            self.car.unlock_doors()
        else:
            self.car.lock_doors()

    def remote_engine(self) -> None:
        """Start or stop engine remotely after PIN validation."""
        if self.entered_pin != self.pin_code:
            print("Incorrect PIN code. Engine start denied.")
            return

        if self.car.engine_started:
            self.car.stop_engine()
        else:
            self.car.start_engine()


def main() -> None:
    """Demonstrate the bridge example."""
    bmw = BMWCar("X5")
    toyota = ToyotaCar("Camry")
    audi = AudiCar("A6")

    remote_1 = StandardRemote(bmw)
    remote_2 = SecureRemote(toyota, "1234")
    remote_3 = StandardRemote(audi)

    print("=== BMW with standard remote ===")
    remote_1.toggle_doors()
    remote_1.toggle_alarm()
    remote_1.remote_engine()
    bmw.show_status()

    print("\n=== Toyota with secure remote ===")
    remote_2.toggle_doors()
    remote_2.toggle_alarm()
    remote_2.enter_pin("1234")
    remote_2.remote_engine()
    toyota.show_status()

    print("\n=== Audi with standard remote ===")
    remote_3.toggle_doors()
    remote_3.remote_engine()
    audi.show_status()


if __name__ == "__main__":
    main()
