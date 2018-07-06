
from importlib import import_module


class TechMockException(Exception):
    pass


class Patch():

    def __init__(self, target):
        self._parse_target(target)

    def _parse_target(self, target):
        module, method = target.rsplit('.', 1)
        self.target = import_module(module)
        self.attribute = method

    def _patch(self):
        self.mock = TechMock()
        self.original = getattr(self.target, self.attribute)
        setattr(self.target, self.attribute, self.mock)

    def _unpatch(self):
        setattr(self.target, self.attribute, self.original)

    def __call__(self, func):
        return self.decorate_callable(func)

    def __enter__(self):
        self._patch()
        return self.mock

    def __exit__(self, *args):
        self._unpatch()

    def decorate_callable(self, func):

        def patched(*args, **kwargs):

            self._patch()
            n_args = args + (self.mock, )

            result = func(*n_args, **kwargs)

            self._unpatch()
            return result

        return patched


class TechMock():

    def __init__(self, return_value=None, parent=None):
        self._children = {}
        self.call_count = 0
        self.call_args = tuple()

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.call_args = self.call_args + (args, kwargs)
        return self

    def __getattr__(self, name):
        child = self._get_child(name)
        return child

    def __repr__(self):
        return '<TechMock id={}>'.format(id(self))

    def _get_child(self, name):
        child = self._children.get(name)
        if not child:
            child = TechMock(parent=self)
            self._children[name] = child

        return child

    def assert_called_once(self):
        if self.call_count == 1:
            raise TechMockException("The {} was called {} times. Expected 1".format(repr(self), self.call_count))
