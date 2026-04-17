from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BurgerType(Enum):
    VEGAN = "vegan"
    CHICKEN = "chicken"
    BEEF = "beef"


class DrinkType(Enum):
    COLD_PEPSI = "cold_pepsi"
    COLD_COCA_COLA = "cold_coca_cola"
    HOT_COFFEE = "hot_coffee"
    HOT_TEA = "hot_tea"


class PackagingType(Enum):
    TO_GO = "to_go"
    ON_SITE = "on_site"


@dataclass(frozen=True)
class Burger:
    btype: BurgerType
    cost: float


@dataclass(frozen=True)
class Drink:
    dtype: DrinkType
    cost: float


@dataclass(frozen=True)
class Packaging:
    ptype: PackagingType
    cost: float


@dataclass(frozen=True)
class Order:
    burger: Burger
    drink: Drink
    packaging: Packaging

    def total_cost(self) -> float:
        return self.burger.cost + self.drink.cost + self.packaging.cost


class OrderBuilder:
    """
    Builder pattern:
    step-by-step sets burger, drink and packaging and then builds the final Order.
    """

    _burger_price = {
        BurgerType.VEGAN: 120.0,
        BurgerType.CHICKEN: 150.0,
        BurgerType.BEEF: 180.0,
    }
    _drink_price = {
        DrinkType.COLD_PEPSI: 50.0,
        DrinkType.COLD_COCA_COLA: 55.0,
        DrinkType.HOT_COFFEE: 60.0,
        DrinkType.HOT_TEA: 45.0,
    }
    _packaging_price = {
        PackagingType.TO_GO: 20.0,
        PackagingType.ON_SITE: 0.0,
    }

    @classmethod
    def burger_prices(cls) -> dict[BurgerType, float]:
        return cls._burger_price.copy()

    @classmethod
    def drink_prices(cls) -> dict[DrinkType, float]:
        return cls._drink_price.copy()

    @classmethod
    def packaging_prices(cls) -> dict[PackagingType, float]:
        return cls._packaging_price.copy()

    def __init__(self) -> None:
        self._burger: Burger | None = None
        self._drink: Drink | None = None
        self._packaging: Packaging | None = None

    def set_burger(self, btype: BurgerType) -> OrderBuilder:
        self._burger = Burger(btype=btype, cost=self._burger_price[btype])
        return self

    def set_drink(self, dtype: DrinkType) -> OrderBuilder:
        self._drink = Drink(dtype=dtype, cost=self._drink_price[dtype])
        return self

    def set_packaging(self, ptype: PackagingType) -> OrderBuilder:
        self._packaging = Packaging(ptype=ptype, cost=self._packaging_price[ptype])
        return self

    def build(self) -> Order:
        if self._burger is None or self._drink is None or self._packaging is None:
            raise ValueError("Order is incomplete: burger, drink, and packaging must be set.")
        return Order(burger=self._burger, drink=self._drink, packaging=self._packaging)


class BurgerCafe:
    """Director-like wrapper for building an Order."""

    @staticmethod
    def create_order(btype: BurgerType, dtype: DrinkType, ptype: PackagingType) -> Order:
        builder = OrderBuilder()
        return builder.set_burger(btype).set_drink(dtype).set_packaging(ptype).build()


def format_menu() -> str:
    burger_prices = OrderBuilder.burger_prices()
    drink_prices = OrderBuilder.drink_prices()
    packaging_prices = OrderBuilder.packaging_prices()

    burger_lines = [
        f"{idx}) {btype.value} - {cost:.0f}"
        for idx, (btype, cost) in enumerate(burger_prices.items(), start=1)
    ]
    drink_lines = [
        f"{idx}) {dtype.value} - {cost:.0f}"
        for idx, (dtype, cost) in enumerate(drink_prices.items(), start=1)
    ]
    packaging_lines = [
        f"{idx}) {ptype.value} - {cost:.0f}"
        for idx, (ptype, cost) in enumerate(packaging_prices.items(), start=1)
    ]
    return (
        "Burgers:\n  "
        + "\n  ".join(burger_lines)
        + "\nDrinks:\n  "
        + "\n  ".join(drink_lines)
        + "\nPackaging:\n  "
        + "\n  ".join(packaging_lines)
    )
