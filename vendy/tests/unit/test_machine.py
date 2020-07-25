from typing import List, Optional

import pytest

from vendy.coin import Coin
from vendy.machine import Dispense, Machine
from vendy.product import Product

p_cola = Product("cola", "1.00")
p_candy = Product("candy", "0.65")
p_chips = Product("candy", "0.50")


class TestMachine:
    @pytest.mark.parametrize("vm", [Machine([(Product(price="1.00"), 1)])])
    @pytest.mark.parametrize(
        "provided, expected_back",
        [
            # reject pennies
            ([Coin.P], [Coin.P]),
            ([Coin.P] * 100, [Coin.P] * 100),
            # reject overpaying
            ([Coin.Q] * 100, [Coin.Q] * 96),
            ([Coin.D] * 100, [Coin.D] * 90),
            ([Coin.N] * 100, [Coin.N] * 80),
            # accept rest
            ([Coin.Q], []),
            ([Coin.D], []),
            ([Coin.N], []),
            ([Coin.Q] * 4, []),
            ([Coin.D] * 10, []),
            ([Coin.N] * 20, []),
            ([Coin.Q, Coin.D, Coin.N], []),
        ],
    )
    def test_insert_coin(
        self, vm: Machine, provided: List[Coin], expected_back: Optional[Coin],
    ) -> None:
        vm = Machine([(Product(price="1.00"), 1)])
        back = list(filter(None, map(vm.insert_coin, provided)))
        assert back == expected_back

    @pytest.mark.parametrize(
        "vm, selection, expected_dispense",
        [
            # no product
            (Machine(), p_cola, (None, [])),
            # product but no quantity
            (Machine([(Product(), 0)]), p_cola, (None, [])),
            # wrong product selected
            (Machine([(p_cola, 1)]), p_chips, (None, []),),
            # not enough funds
            (Machine([(p_cola, 1)]), p_cola, (None, []),),
            # product returned & largest possible change given back
            (
                Machine(
                    [(p_candy, 1)],
                    [(Coin.Q, 10), (Coin.D, 10), (Coin.N, 10)],
                    pending=[Coin.Q] * 4,
                ),
                p_candy,
                (p_candy, [Coin.Q, Coin.D]),
            ),
        ],
    )
    def test_select_product(
        self, vm: Machine, selection: Product, expected_dispense: Dispense,
    ) -> None:
        assert vm.select_product(selection) == expected_dispense

    # TODO FIX
    @pytest.mark.parametrize(
        "vm, expected",
        [(Machine(pending=[]), []), (Machine(pending=[Coin.Q]), [Coin.Q])],
    )
    def test_return_coins(self, vm: Machine, expected: List[Coin]) -> None:
        assert vm.return_coins() == expected

    @pytest.mark.parametrize(
        "vm, expected_display",
        [
            (Machine(display="THANK YOU"), "EXACT CHANGE ONLY"),
            (Machine(display="SOLD OUT"), "EXACT CHANGE ONLY"),
            # has change
            (
                Machine([(p_cola, 1)], [(Coin.N, 100)], display="THANK YOU"),
                "INSERT COINS",
            ),
            (
                Machine([(p_cola, 0)], [(Coin.N, 100)], display="SOLD OUT"),
                "INSERT COINS",
            ),
            # has change with pending total
            (
                Machine(
                    [(p_cola, 0)], [(Coin.N, 100)], display="SOLD OUT", pending=[Coin.Q]
                ),
                "$0.25",
            ),
            # no change
            (
                Machine([(p_cola, 0)], [(Coin.Q, 4)], display="SOLD OUT"),
                "EXACT CHANGE ONLY",
            ),
            (Machine(display="SOLD OUT", pending=[Coin.Q]), "$0.25"),
        ],
    )
    def test_display(self, vm: Machine, expected_display: str,) -> None:
        vm.check_display()  # cycle once
        assert vm.check_display() == expected_display
