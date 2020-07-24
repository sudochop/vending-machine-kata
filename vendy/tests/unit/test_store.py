import types

from vendy.store import Store


class TestStore:
    """
    Not used anywhere.
    Just for sake of completion/coverage.
    """

    def test_remove(self) -> None:
        store: Store = types.new_class("S", [Store[str]])()
        store.add("foo", 0)
        assert store.items.get("foo") is not None
        store.remove("foo")
        assert store.items.get("foo") is None
