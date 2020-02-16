from typing import List


class Accessor:
    def get(self, obj):
        raise NotImplementedError

    def set(self, obj, value):
        raise NotImplementedError


class PropertyAccessor(Accessor):
    def __init__(self, property_name: str):
        self.property_name = property_name

    def get(self, obj):
        return getattr(obj, self.property_name)

    def set(self, obj, value):
        setattr(obj, self.property_name, value)
        return obj

    def __repr__(self):
        return ".{}".format(self.property_name)


class KeyAccessor(Accessor):
    def __init__(self, index):
        self.index = index

    def get(self, obj):
        return obj[self.index]

    def set(self, obj, value):
        obj[self.index] = value
        return obj

    def __repr__(self):
        return "[{}]".format(self.index)


class TupleAccessor(KeyAccessor):
    def set(self, obj, value):
        obj = list(obj)
        obj[self.index] = value
        return tuple(obj)

    def __repr__(self):
        return "({})".format(self.index)


class DummyAccessor(Accessor):
    def get(self, obj):
        return obj

    def set(self, obj, value):
        return value

    def __repr__(self):
        return ""


class NestedAccessor(Accessor):
    def __init__(self, a: Accessor, b: Accessor):
        self.a = a
        self.b = b

    def get(self, obj):
        return self.b.get(self.a.get(obj))

    def set(self, obj, value):
        inner = self.a.get(obj)
        new_inner = self.b.set(inner, value)
        return self.a.set(obj, new_inner)

    @classmethod
    def from_list(cls, ls: List[Accessor]) -> Accessor:
        if len(ls) == 1:
            return ls[0]
        return NestedAccessor(ls[0], cls.from_list(ls[1:]))

    def __repr__(self):
        return "{}{}".format(repr(self.a), repr(self.b))
