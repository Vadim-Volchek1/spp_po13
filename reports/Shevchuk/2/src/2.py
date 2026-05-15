# pylint: disable=invalid-name
"""Lab 2, task 2, variant 7.

Bus depot system model.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Person(ABC):
    """Base class for people in the system."""

    def __init__(self, name: str) -> None:
        """Initialize person with name."""
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self.name = name

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __eq__(self, other: object) -> bool:
        """Compare people by type and name."""
        return isinstance(other, self.__class__) and self.name == other.name


class Vehicle(ABC):
    """Abstract base class for depot vehicles."""

    def __init__(self, vehicle_id: str, model: str) -> None:
        """Initialize vehicle."""
        if not vehicle_id.strip():
            raise ValueError("Vehicle id cannot be empty.")
        if not model.strip():
            raise ValueError("Model cannot be empty.")

        self.vehicle_id = vehicle_id
        self.model = model
        self.is_available = True
        self.needs_repair = False

    @abstractmethod
    def vehicle_type(self) -> str:
        """Return vehicle type."""

    def mark_repair_needed(self) -> None:
        """Mark vehicle as requiring repair."""
        self.needs_repair = True
        self.is_available = False

    def mark_serviceable(self) -> None:
        """Mark vehicle as ready for work."""
        self.needs_repair = False
        self.is_available = True

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"{self.vehicle_type()}(id='{self.vehicle_id}', model='{self.model}', "
            f"available={self.is_available}, needs_repair={self.needs_repair})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare vehicles by type and identifier."""
        return isinstance(other, self.__class__) and self.vehicle_id == other.vehicle_id


# pylint: disable=too-few-public-methods
class Car(Vehicle):
    """Concrete vehicle used for trips."""

    def vehicle_type(self) -> str:
        """Return vehicle type."""
        return "Car"


class WorkerAction(ABC):
    """Interface-like abstract class for worker actions."""

    @abstractmethod
    def perform_action(self) -> str:
        """Perform and describe an action."""


# pylint: disable=too-few-public-methods
@dataclass
class TripRequest:
    """Represent a request for a trip."""

    route_name: str
    cargo_description: str
    assigned: bool = False


# pylint: disable=too-few-public-methods
@dataclass
class RepairRequest:
    """Represent a driver's repair request."""

    driver_name: str
    vehicle_id: str
    description: str
    completed: bool = False


class Trip(WorkerAction):
    """Represent a trip assigned to a driver and a vehicle."""

    def __init__(self, request: TripRequest, driver: Driver, vehicle: Vehicle) -> None:
        """Initialize trip."""
        self.request = request
        self.driver = driver
        self.vehicle = vehicle
        self.completed = False
        self.vehicle_condition = "unknown"

    def complete(self, vehicle_condition: str) -> None:
        """Complete the trip and save vehicle condition."""
        self.completed = True
        self.vehicle_condition = vehicle_condition
        self.vehicle.is_available = True

    def perform_action(self) -> str:
        """Describe trip execution."""
        return (
            f"Trip on route '{self.request.route_name}' is assigned to {self.driver.name} "
            f"using vehicle {self.vehicle.vehicle_id}."
        )

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"Trip(route='{self.request.route_name}', driver='{self.driver.name}', "
            f"vehicle='{self.vehicle.vehicle_id}', completed={self.completed}, "
            f"condition='{self.vehicle_condition}')"
        )

    def __eq__(self, other: object) -> bool:
        """Compare trips by request, driver and vehicle."""
        if not isinstance(other, Trip):
            return False

        return (
            self.request.route_name == other.request.route_name
            and self.driver == other.driver
            and self.vehicle == other.vehicle
        )


class Driver(Person):
    """Represent a driver."""

    def __init__(self, name: str) -> None:
        """Initialize driver."""
        super().__init__(name)
        self.is_suspended = False
        self.current_trip: Trip | None = None

    def request_repair(self, vehicle: Vehicle, description: str) -> RepairRequest:
        """Create a repair request for a vehicle."""
        if not description.strip():
            raise ValueError("Repair description cannot be empty.")

        vehicle.mark_repair_needed()
        return RepairRequest(self.name, vehicle.vehicle_id, description)

    def assign_trip(self, trip: Trip) -> None:
        """Assign trip to driver."""
        if self.is_suspended:
            raise ValueError("Suspended driver cannot be assigned to a trip.")
        self.current_trip = trip

    def complete_trip(self, vehicle_condition: str) -> None:
        """Complete current trip."""
        if self.current_trip is None:
            raise ValueError("Driver has no assigned trip.")

        self.current_trip.complete(vehicle_condition)
        self.current_trip = None

    def __str__(self) -> str:
        """Return string representation."""
        return f"Driver(name='{self.name}', suspended={self.is_suspended})"


class Dispatcher(Person):
    """Represent a dispatcher."""

    def assign_trip(
        self,
        request: TripRequest,
        driver: Driver,
        vehicle: Vehicle,
    ) -> Trip:
        """Assign request to a driver and a vehicle."""
        if request.assigned:
            raise ValueError("Trip request is already assigned.")
        if driver.is_suspended:
            raise ValueError("Driver is suspended.")
        if not vehicle.is_available or vehicle.needs_repair:
            raise ValueError("Vehicle is not available.")

        request.assigned = True
        vehicle.is_available = False
        trip = Trip(request, driver, vehicle)
        driver.assign_trip(trip)
        return trip

    def suspend_driver(self, driver: Driver) -> None:
        """Suspend a driver from work."""
        driver.is_suspended = True

    def restore_driver(self, driver: Driver) -> None:
        """Restore a driver to work."""
        driver.is_suspended = False

    def __str__(self) -> str:
        """Return string representation."""
        return f"Dispatcher(name='{self.name}')"


class BusDepot:
    """Represent bus depot system."""

    def __init__(self, name: str) -> None:
        """Initialize depot."""
        if not name.strip():
            raise ValueError("Depot name cannot be empty.")

        self.name = name
        self.drivers: list[Driver] = []
        self.vehicles: list[Vehicle] = []
        self.trip_requests: list[TripRequest] = []
        self.repair_requests: list[RepairRequest] = []
        self.trips: list[Trip] = []

    def add_driver(self, driver: Driver) -> None:
        """Add driver to depot."""
        if driver not in self.drivers:
            self.drivers.append(driver)

    def add_vehicle(self, vehicle: Vehicle) -> None:
        """Add vehicle to depot."""
        if vehicle not in self.vehicles:
            self.vehicles.append(vehicle)

    def add_trip_request(self, request: TripRequest) -> None:
        """Add trip request."""
        self.trip_requests.append(request)

    def add_repair_request(self, request: RepairRequest) -> None:
        """Add repair request."""
        self.repair_requests.append(request)

    def add_trip(self, trip: Trip) -> None:
        """Add trip to history."""
        self.trips.append(trip)

    def __str__(self) -> str:
        """Return string representation."""
        return (
            f"BusDepot(name='{self.name}', drivers={len(self.drivers)}, "
            f"vehicles={len(self.vehicles)}, trip_requests={len(self.trip_requests)}, "
            f"repair_requests={len(self.repair_requests)}, trips={len(self.trips)})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare depots by name."""
        return isinstance(other, BusDepot) and self.name == other.name


def main() -> None:
    """Demonstrate bus depot system."""
    depot = BusDepot("City Bus Depot")
    dispatcher = Dispatcher("Ivan Petrov")
    driver = Driver("Sergey Ivanov")
    vehicle = Car("A-101", "MAZ-203")

    depot.add_driver(driver)
    depot.add_vehicle(vehicle)

    trip_request = TripRequest("Minsk-Brest", "Passengers")
    depot.add_trip_request(trip_request)

    trip = dispatcher.assign_trip(trip_request, driver, vehicle)
    depot.add_trip(trip)

    print(depot)
    print(dispatcher)
    print(driver)
    print(vehicle)
    print(trip.perform_action())

    driver.complete_trip("Serviceable")
    print("Trip completed.")
    print(vehicle)

    repair_request = driver.request_repair(vehicle, "Brake system inspection required")
    depot.add_repair_request(repair_request)

    print("Repair request created:")
    print(repair_request)

    dispatcher.suspend_driver(driver)
    print("Driver suspended:", driver)


if __name__ == "__main__":
    main()
