from decimal import Decimal
from typing import List, Optional

from .coin import Coin
from .store import Store


class Register(Store[Coin]):
    def deposit(self, coins: List[Coin], /) -> None:
        for coin in coins:
            self.increment(coin)

    def can_make_change(self, amount: Decimal, /) -> bool:
        """
        Check ahead of time if change can be made.
        """
        if amount <= Decimal("0.00"):
            return False
        return self.make_change(amount, False) is not None

    def make_change(
        self, amount: Decimal, /, withdraw: bool = True
    ) -> Optional[List[Coin]]:
        """
        Attempt to make change from current inventory.

        * Change will be provided in the largest coins possible.
        * If only partial change can be created, None is returned.
        """

        change = []

        while amount > 0:
            if (
                coin := self._get_largest_coin(Coin.Q, amount)
                or self._get_largest_coin(Coin.D, amount)
                or self._get_largest_coin(Coin.N, amount)
            ) :
                change.append(coin)
                amount = amount - coin.value
                self.decrement(coin)
                continue
            return None

        if not withdraw:
            for coin in change:
                self.increment(coin)

        return change

    def _get_largest_coin(self, coin: Coin, amount: Decimal, /) -> Optional[Coin]:
        if amount >= coin.value and self.is_available(coin):
            return coin
        return None
