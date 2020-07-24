from decimal import Decimal
from typing import Iterable


def frange(start: Decimal, stop: Decimal, step: Decimal) -> Iterable[Decimal]:
    """
    Since range() doesn't support floats.
    """
    total = start
    while total <= stop:
        yield total
        total = total + step
