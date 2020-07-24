from vendy.coin import Coin
from vendy.machine import Machine
from vendy.product import Product


class TestInteraction:
    def test_empty_machine(self) -> None:
        vm = Machine()

        assert vm.check_display() == "EXACT CHANGE ONLY"

        product = Product("cola", "0.65")

        assert vm.insert_coin(Coin.Q) == Coin.Q
        assert vm.select_product(product) == (None, [])
        assert vm.check_display() == "SOLD OUT"

        assert vm.return_coins() == []
        assert vm.check_display() == "EXACT CHANGE ONLY"

        assert vm.select_product(product) == (None, [])
        assert vm.check_display() == "SOLD OUT"
        assert vm.check_display() == "EXACT CHANGE ONLY"

    def test_successful_transaction(self) -> None:
        p_cola = Product("cola", "1.00")
        p_candy = Product("candy", "0.65")
        p_chips = Product("chips", "0.50")

        vm = Machine(
            [(p_cola, 100), (p_candy, 100), (p_chips, 100)],
            [(Coin.Q, 100), (Coin.D, 100), (Coin.N, 100)],
        )

        assert vm.check_display() == "INSERT COINS"
        assert vm.select_product(p_cola) == (None, [])
        assert vm.check_display() == "PRICE $1.00"

        assert vm.insert_coin(Coin.P) == Coin.P
        assert vm.return_coins() == []
        assert vm.check_display() == "INSERT COINS"

        assert vm.insert_coin(Coin.Q) is None
        assert vm.check_display() == "$0.25"
        assert vm.return_coins() == [Coin.Q]
        assert vm.check_display() == "INSERT COINS"

        for coin in [Coin.Q] * 2 + [Coin.D] * 2 + [Coin.N] * 2:
            assert vm.insert_coin(coin) is None

        assert vm.check_display() == "$0.80"
        assert vm.select_product(p_chips) == (p_chips, [Coin.Q, Coin.N])
        assert vm.check_display() == "THANK YOU"
        assert vm.check_display() == "INSERT COINS"
