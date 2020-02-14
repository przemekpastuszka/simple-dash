from simpledash.inspector.accessors import TupleAccessor, NestedAccessor, KeyAccessor, DummyAccessor, PropertyAccessor


def test_key_accessor():
    accessor = KeyAccessor(1)
    assert accessor.get(["a", "b", "c"]) == "b"
    assert accessor.set(["a", "b", "c"], "B") == ["a", "B", "c"]


def test_tuple_accessor():
    accessor = TupleAccessor(1)
    assert accessor.get(("a", "b", "c")) == "b"
    assert accessor.set(("a", "b", "c"), "B") == ("a", "B", "c")


def test_property_accessor():
    accessor = PropertyAccessor('index')

    assert accessor.get(KeyAccessor(1)) == 1
    assert accessor.set(KeyAccessor(1), 2).index == 2


def test_nested_accessor():
    accessor = NestedAccessor(TupleAccessor(1), TupleAccessor(2))
    assert accessor.get(("a", ("x", "y", "z"))) == "z"
    assert accessor.set(("a", ("x", "y", "z")), "Z") == ("a", ("x", "y", "Z"))


def test_nested_accessor_with_dummy():
    for accessor in [
        NestedAccessor(DummyAccessor(), TupleAccessor(0)),
        NestedAccessor(TupleAccessor(0), DummyAccessor())
    ]:
        assert accessor.get(("a", ("x", "y"))) == "a"
        assert accessor.set(("a", ("x", "y")), "A") == ("A", ("x", "y"))


def test_dummy_accessor():
    accessor = DummyAccessor()
    assert accessor.set("a", "b") == "b"
