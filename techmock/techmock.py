
from importlib import import_module


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

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return '<TechMock id={}>'.format(id(self))
