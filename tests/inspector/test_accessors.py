from simpledash.inspector.accessors import TupleAccessor, NestedAccessor
from simpledash.inspector.component import KeyAccessor


def test_key_accessor():
    accessor = KeyAccessor(1)
    assert accessor.get(["a", "b", "c"]) == "b"
    assert accessor.set(["a", "b", "c"], "B") == ["a", "B", "c"]


def test_tuple_accessor():
    accessor = TupleAccessor(1)
    assert accessor.get(("a", "b", "c")) == "b"
    assert accessor.set(("a", "b", "c"), "B") == ("a", "B", "c")


def test_nested_accessor():
    accessor = NestedAccessor(TupleAccessor(1), TupleAccessor(2))
    assert accessor.get(("a", ("x", "y", "z"))) == "z"
    assert accessor.set(("a", ("x", "y", "z")), "Z") == ("a", ("x", "y", "Z"))
