from decimal import Decimal
from typing import List

import pytest

from vendy.coin import Coin
from vendy.register import Register

D = Decimal


class TestRegister:
    @pytest.mark.parametrize(
        "coin, expected", [(Coin.N, 0), (Coin.D, 10), (Coin.Q, 100)]
    )
    def test_deposit(self, coin: Coin, expected: int) -> None:
        register = Register()
        register.add(coin, 0)
        register.deposit([coin] * expected)
        assert register.items[coin] == expected

    @pytest.mark.parametrize(
        "provided, amounts, expected",
        [
            # No funds
            ([], [D("0.00"), D("0.05")], False),
            # Not enough funds
            ([Coin.Q], [D("0.30")], False),
            # Enough funds but not the right coins
            ([Coin.Q] * 2, [D("0.05"), D("0.30")], False),
            # Enough funds and the right coins
            (
                [Coin.Q, Coin.D, Coin.N],
                [D("0.15"), D("0.30"), D("0.35"), D("0.40")],
                True,
            ),
        ],
    )
    def test_can_make_change(
        self, provided: List[Coin], amounts: List[Decimal], expected: bool
    ) -> None:
        register = Register()
        for coin in provided:
            register.add(coin, 0)
        for coin in provided:
            register.increment(coin)
        for amount in amounts:
            assert register.can_make_change(amount) == expected

    @pytest.mark.parametrize(
        "amount, expected",
        [
            (D("0.15"), [Coin.D, Coin.N]),
            (D("0.40"), [Coin.Q, Coin.D, Coin.N]),
            (D("1.00"), [Coin.Q] * 4),
        ],
    )
    def test_make_change(self, amount: Decimal, expected: List[Coin]) -> None:
        register = Register()
        register.add(Coin.Q, 0)
        register.add(Coin.D, 0)
        register.add(Coin.N, 0)

        for coin in expected:
            register.increment(coin)

        assert register.make_change(amount) == expected
        assert register.make_change(amount) is None  # ensure removed
