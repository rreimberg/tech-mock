
def _format_call_signature(name, args, kwargs):
    formatted_args = ''
    args_string = ', '.join([repr(arg) for arg in args])
    kwargs_string = ', '.join(["{}={}".format(key, repr(value)) for key, value in kwargs.items()])

    if args_string:
        formatted_args = args_string
    if kwargs_string:
        if formatted_args:
            formatted_args += ', '
        formatted_args += kwargs_string

    return "{}({})".format(name, formatted_args)


class TechMock():

    def __init__(self, name=None, parent=None):
        self._name = name
        self._children = {}
        self.call_count = 0
        self.call_args = tuple()
        self.call_args_list = []

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.call_args = (args, kwargs)
        self.call_args_list.append(self.call_args)

        return_value = getattr(self, 'return_value', self)
        return return_value

    def __getattr__(self, name):
        child = self._get_child(name)
        return child

    def __repr__(self):
        return '<TechMock id={} - {}>'.format(id(self), self._mock_name)

    @property
    def _mock_name(self):
        if not self._name:
            return 'mock'

        return self._name

    def _get_child(self, name):
        child = self._children.get(name)
        if not child:
            child = TechMock(parent=self, name='{}.{}'.format(self._mock_name, name))
            self._children[name] = child

        return child

    def assert_not_called(self):
        if self.call_count > 0:
            raise AssertionError("Expected '{}' to not have been called. Called {} times.".format(self._mock_name, self.call_count))

    def assert_called(self):
        if self.call_count == 0:
            raise AssertionError("Expected '{}' to have been called".format(self._mock_name))

    def assert_called_once(self):
        self.assert_called()

        if self.call_count > 1:
            raise AssertionError("Expected '{}' to have been called once. Called {} times.".format(self._mock_name))

    def assert_called_with(self, *args, **kwargs):
        expected = (args, kwargs)
        if self.call_args != expected:
            raise AssertionError("Expected call: {}\nNot called".format(expected))

    def assert_called_once_with(self, *args, **kwargs):
        self.assert_called_once()
        self.assert_called_with(*args, **kwargs)

#    def assert_has_calls(self, calls):
#        'Calls not found.\nExpected: %r\n'
#        'Actual: %r' % (_CallList(calls), self.mock_calls)

    def assert_any_call(self, *args, **kwargs):
        expected = (args, kwargs)
        if expected not in self.call_args_list:
            expected_string = _format_call_signature(self._mock_name, args, kwargs)
            raise AssertionError("{} call not found".format(expected_string))
