from decimal import Decimal
from enum import Enum
from typing import List, Optional, cast

D = Decimal


class Coin(Enum):
    P = Decimal("0.01")
    N = Decimal("0.05")
    D = Decimal("0.10")
    Q = Decimal("0.25")


def from_spec(
    weight: Decimal, diameter: Decimal, thickness: Decimal, /
) -> Optional[Coin]:
    """Convert the specifications to a Coin."""
    weightmap = {
        (D("2.500"), D("19.05"), D("1.52")): Coin.P,
        (D("5.000"), D("21.21"), D("1.95")): Coin.N,
        (D("2.268"), D("17.91"), D("1.35")): Coin.D,
        (D("5.670"), D("24.26"), D("1.75")): Coin.Q,
    }

    return weightmap.get((weight, diameter, thickness))


def coin_total(coins: List[Coin]) -> Decimal:
    """Calculate the decimal representation of a list of coins."""
    return D(sum(map(lambda c: cast(Decimal, c.value), coins)))
