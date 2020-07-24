from decimal import Decimal
from typing import List

import pytest

from vendy.coin import Coin, coin_total, from_spec

D = Decimal


@pytest.mark.parametrize(
    "weight, diameter, thickness, expected",
    [
        (D("2.500"), D("19.05"), D("1.52"), Coin.P),
        (D("5.000"), D("21.21"), D("1.95"), Coin.N),
        (D("2.268"), D("17.91"), D("1.35"), Coin.D),
        (D("5.670"), D("24.26"), D("1.75"), Coin.Q),
    ],
)
def test_from_spec(
    weight: Decimal, diameter: Decimal, thickness: Decimal, expected: Coin
) -> None:
    eps = D("1E-27")

    assert from_spec(weight, diameter, thickness) is expected
    assert from_spec(weight + eps, diameter + eps, thickness + eps) is None
    assert from_spec(weight - eps, diameter - eps, thickness - eps) is None


@pytest.mark.parametrize(
    "coins, expected",
    [
        ([], Decimal("0.00")),
        ([Coin.Q] * 4, Decimal("1.00")),
        ([Coin.Q, Coin.D, Coin.N], Decimal("0.40")),
    ],
)
def test_coin_total(coins: List[Coin], expected: Decimal) -> None:
    assert coin_total(coins) == expected
