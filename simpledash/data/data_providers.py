import operator
from typing import Set, Dict, Any, Union

from dash.dependencies import Input


class DataProviderOperationException(Exception):
    pass


class DataProvider:
    def depends_on(self) -> Set[Input]:
        raise NotImplementedError

    def evaluate(self, context: Dict[Input, Any]):
        raise NotImplementedError

    def __getattr__(self, x) -> 'DataProvider':
        return Operation(getattr, self, x)

    def __getitem__(self, item) -> 'DataProvider':
        return Operation(operator.getitem, self, item)

    def __call__(self, *args, **kwargs) -> 'DataProvider':
        return Operation(lambda obj, *a, **kw: obj(*a, **kw), self, *args, **kwargs)

    def __bool__(self):
        raise DataProviderOperationException("Truth value of data provider is undefined")

    def __eq__(self, other):
        raise DataProviderOperationException("Equality of a data provider cannot be determined")

    def __iter__(self):
        raise DataProviderOperationException("Iteration over data provider is forbidden")

    def __setitem__(self, key, value):
        raise DataProviderOperationException("Assignment to data provider is forbidden")

    @classmethod
    def to_provider(cls, v) -> 'DataProvider':
        if isinstance(v, DataProvider):
            return v
        if isinstance(v, Input):
            return DashInput(v)
        return StaticValueProvider(v)


class StaticValueProvider(DataProvider):
    def __init__(self, value):
        self.value = value

    def depends_on(self) -> Set[Input]:
        return set()

    def evaluate(self, context: Dict[Input, Any]):
        return self.value


class Operation(DataProvider):
    def __init__(self, op, *args, **kwargs):
        self._op = op
        self._args = tuple(DataProvider.to_provider(v) for v in args)
        self._kwargs = {k: DataProvider.to_provider(arg) for k, arg in kwargs.items()}

        self._depends_on = set()
        for arg in list(self._args) + list(self._kwargs.values()):
            self._depends_on |= arg.depends_on()

    def depends_on(self) -> Set[Input]:
        return self._depends_on

    def evaluate(self, context: Dict[Input, Any]):
        args = tuple(arg.evaluate(context) for arg in self._args)
        kwargs = {k: arg.evaluate(context) for k, arg in self._kwargs.items()}
        return self._op(*args, **kwargs)


def data_provider(*args: Union[Input, DataProvider], **kwargs: Union[Input, DataProvider]):
    def wrap(f):
        return MethodProxy(f, *args, **kwargs)

    return wrap


class MethodProxy(Operation):
    def __init__(self, op, *args, **kwargs):
        super().__init__(op, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._op(*args, **kwargs)


class DashInput(DataProvider):
    def __init__(self, dash_input: Input):
        self._dash_input = dash_input

    def evaluate(self, context: Dict[Input, Any]):
        return context[self._dash_input]

    def depends_on(self) -> Set[Input]:
        return {self._dash_input}

