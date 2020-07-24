from decimal import Decimal
from typing import List, Optional, Tuple

from .coin import Coin, coin_total
from .inventory import Inventory
from .product import Product
from .register import Register
from .utils import frange

Dispense = Tuple[Optional[Product], List[Coin]]


class Machine:
    """
    Vending Machine API
    """

    def __init__(
        self,
        products: List[Tuple[Product, int]] = None,
        bank: List[Tuple[Coin, int]] = None,
        pending: List[Coin] = None,
        display: str = "",
    ) -> None:
        self.inventory = Inventory()
        self.register = Register()
        self.pending = pending or []
        self.display = display

        for (product, amount) in products or []:
            self.inventory.add(product, amount)
        for (coin, amount) in bank or []:
            self.register.add(coin, amount)
        self.display = self._insert_display_text

    def insert_coin(self, coin: Coin) -> Optional[Coin]:
        """
        Provide funding for future transactions.
        """

        # Reject pennies.
        if coin is Coin.P:
            return coin

        # Prevent overpaying.
        if self.pending_total >= max(self.prices or [Decimal("0.00")]):
            return coin

        self.pending.append(coin)
        self.display = f"{format_price(self.pending_total)}"

        return None

    def select_product(self, product: Product) -> Dispense:
        """
        Attempt to purchase an product.
        """

        if not self.inventory.is_available(product):
            self.display = "SOLD OUT"
            return (None, [])

        if self.pending_total < product.price:
            self.display = f"PRICE {format_price(product.price)}"
            return (None, [])

        self.inventory.decrement(product)
        self.register.deposit(self.pending)

        remaining = self.pending_total - product.price
        change = self.register.make_change(remaining) or []  # they were warned..

        self.pending = []
        self.display = "THANK YOU"

        return (product, change)

    def return_coins(self) -> List[Coin]:
        coins = self.pending
        self.pending = []
        self.display = self._insert_display_text
        return coins

    def check_display(self) -> str:
        """
        Return the current display and update for future checks.
        """

        lastdisplay = self.display

        if self.pending:
            self.display = format_price(self.pending_total)

        else:
            self.display = self._insert_display_text

        return lastdisplay

    @property
    def pending_total(self) -> Decimal:
        """
        Convert the pending coin list to a decimal.
        """
        return coin_total(self.pending)

    @property
    def can_make_change(self) -> bool:
        """
        The maximum change required is the difference in price
        between the most and least expensive items + 0.20.
        Every 0.05 increment must be dispensable.
        """
        if (prices := self.prices) :
            amount = max(prices) - min(prices) + Decimal("0.20")
            change_needed = list(frange(Decimal("0.05"), amount, Decimal("0.05")))
            change_made = map(lambda c: self.register.can_make_change(c), change_needed)
            return False not in change_made
        return False

    @property
    def prices(self) -> List[Decimal]:
        """
        List of product prices.
        """
        return list(map(lambda p: p.price, self.inventory.items.keys()))

    @property
    def _insert_display_text(self) -> str:
        if self.pending_total > 0.0:
            return format_price(self.pending_total)
        else:
            return "INSERT COINS" if self.can_make_change else "EXACT CHANGE ONLY"


def format_price(price: Decimal) -> str:
    return f"${price:0,.2f}"
