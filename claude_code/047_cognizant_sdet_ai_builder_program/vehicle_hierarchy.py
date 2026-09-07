"""Vehicle -> Car -> ElectricCar hierarchy: super(), overriding, and MRO practice."""

from __future__ import annotations


class Vehicle:
    """Base class: common vehicle identity and info."""

    def __init__(self, make: str, model: str, year: int) -> None:
        self.make = make
        self.model = model
        self.year = year

    def get_info(self) -> str:
        return f"{self.year} {self.make} {self.model}"


class Car(Vehicle):
    """Adds num_doors to the base vehicle identity."""

    def __init__(self, make: str, model: str, year: int, num_doors: int) -> None:
        # super().__init__() runs Vehicle.__init__ (the next class in the MRO),
        # so make/model/year are set exactly once by the class that owns them.
        # It is called FIRST so subclass additions build on initialized state.
        super().__init__(make, model, year)
        self.num_doors = num_doors

    def get_info(self) -> str:
        # Method OVERRIDING: same name/signature as Vehicle.get_info, new behavior.
        # super().get_info() reuses the parent's text instead of duplicating it,
        # then this level appends what only Car knows about.
        return f"{super().get_info()} | {self.num_doors} doors"


class ElectricCar(Car):
    """Adds battery_range; demonstrates a 3-level super() chain."""

    def __init__(self, make: str, model: str, year: int, num_doors: int, battery_range: int) -> None:
        # This super() call resolves to Car.__init__ per the MRO
        # (ElectricCar -> Car -> Vehicle -> object), and Car's own super() call
        # continues the chain up to Vehicle. One call here initializes all 3 levels.
        super().__init__(make, model, year, num_doors)
        self.battery_range = battery_range

    def get_info(self) -> str:
        # Overriding again: Car.get_info already includes Vehicle's text, so the
        # full chain is composed by each level calling super().get_info().
        return f"{super().get_info()} | {self.battery_range} mi range"


if __name__ == "__main__":
    vehicles = [
        Vehicle("Honda", "Civic", 2020),
        Car("Toyota", "Camry", 2022, 4),
        ElectricCar("Tesla", "Model 3", 2024, 4, 272),
    ]

    # Polymorphism: one loop, one method name, different behavior per class.
    # Each call resolves via the object's own class first (MRO), so ElectricCar's
    # get_info runs for the Tesla even though the list is typed by the base concept.
    for vehicle in vehicles:
        print(vehicle.get_info())

    print("\nMRO for ElectricCar:")
    for cls in ElectricCar.__mro__:
        print(" ", cls.__name__)
