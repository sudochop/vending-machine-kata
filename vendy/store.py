from dataclasses import dataclass, field
from typing import Dict, Generic, TypeVar

T = TypeVar("T")


@dataclass
class Store(Generic[T]):
    """
    Storage interface.
    Used for Register and Inventory.
    """

    items: Dict[T, int] = field(default_factory=dict)

    def add(self, item: T, quantity: int) -> None:
        self.items[item] = quantity

    def remove(self, item: T) -> None:
        self.items.pop(item)

    def increment(self, item: T) -> None:
        self.items[item] = self.items[item] + 1

    def decrement(self, item: T) -> None:
        if self.is_available(item):
            self.items[item] = self.items[item] - 1

    def is_available(self, item: T) -> bool:
        return self.items.get(item, 0) > 0
