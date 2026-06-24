import sys

class TestResult:
    def __init__(self):
        self.tests_run = 0
        self.failures = 0
        self.errors = 0
        self.successes = 0

    def add_success(self):
        self.tests_run += 1
        self.successes += 1

    def add_failure(self, test_name, message):
        self.tests_run += 1
        self.failures += 1
        print(f"FAIL: {test_name}")
        print(f"  {message}")

    def add_error(self, test_name, message):
        self.tests_run += 1
        self.errors += 1
        print(f"ERROR: {test_name}")
        print(f"  {message}")

    def summary(self):
        print(f"\n{'='*50}")
        print(f"Tests run: {self.tests_run}")
        print(f"Successes: {self.successes}")
        print(f"Failures: {self.failures}")
        print(f"Errors: {self.errors}")
        return self.failures == 0 and self.errors == 0


class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self, result):
        try:
            method = getattr(self, self.name)
            method()
            result.add_success()
        except AssertionError as e:
            result.add_failure(self.name, str(e))
        except Exception as e:
            result.add_error(self.name, str(e))


class TestSuite:
    def __init__(self):
        self.tests = []

    def add_test(self, test_class):
        for method_name in dir(test_class):
            if method_name.startswith('test_'):
                self.tests.append((test_class, method_name))

    def run(self):
        result = TestResult()
        for test_class, method_name in self.tests:
            test_instance = test_class(method_name)
            test_instance.run(result)
        return result


def assert_equal(a, b):
    if a != b:
        raise AssertionError(f"{a} != {b}")


def assert_true(x):
    if not x:
        raise AssertionError(f"{x} is not truthy")


def assert_false(x):
    if x:
        raise AssertionError(f"{x} is not falsy")


def assert_raises(exc_class, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError(f"Expected {exc_class.__name__} was not raised")
    except exc_class:
        pass


class SimpleMock:
    def __init__(self):
        self.calls = []
        self.return_values = {}
        self.side_effects = {}

    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        key = (args, tuple(sorted(kwargs.items())) if kwargs else ())
        if key in self.side_effects:
            raise self.side_effects[key]
        return self.return_values.get(key, None)

    def when_called_with(self, *args, **kwargs):
        return _MockSetter(self, args, kwargs)

    def set_return_value(self, args, kwargs, value):
        key = (args, tuple(sorted(kwargs.items())) if kwargs else ())
        self.return_values[key] = value

    def set_side_effect(self, args, kwargs, exception):
        key = (args, tuple(sorted(kwargs.items())) if kwargs else ())
        self.side_effects[key] = exception

    def assert_called_once_with(self, *args, **kwargs):
        if len(self.calls) != 1:
            raise AssertionError(f"Expected 1 call, got {len(self.calls)}")
        if self.calls[0] != (args, kwargs):
            raise AssertionError(f"Expected {args}, {kwargs}, got {self.calls[0]}")


class _MockSetter:
    def __init__(self, mock, args, kwargs):
        self.mock = mock
        self.args = args
        self.kwargs = kwargs

    def then_return(self, value):
        self.mock.set_return_value(self.args, self.kwargs, value)
        return self.mock

    def then_raise(self, exception):
        self.mock.set_side_effect(self.args, self.kwargs, exception)
        return self.mock


class FixtureStore:
    def __init__(self):
        self.fixtures = {}
        self.scope = {}

    def register(self, name, func, scope="function"):
        self.fixtures[name] = func
        self.scope[name] = scope

    def get(self, name):
        return self.fixtures[name]()

    def clear_function_scope(self):
        for name, s in self.scope.items():
            if s == "function":
                pass


class SampleTests(TestCase):
    def test_math(self):
        assert_equal(1 + 1, 2)

    def test_string(self):
        assert_equal("hello".upper(), "HELLO")

    def test_list(self):
        lst = [1, 2, 3]
        assert_true(len(lst) == 3)

    def test_mock(self):
        mock = SimpleMock()
        mock.when_called_with(1, 2).then_return(3)
        result = mock(1, 2)
        assert_equal(result, 3)

    def test_mock_call_tracking(self):
        mock = SimpleMock()
        mock(1)
        mock(2)
        assert_equal(len(mock.calls), 2)


def demo():
    print("=== Simple Test Runner Demo ===")
    suite = TestSuite()
    suite.add_test(SampleTests)
    result = suite.run()
    result.summary()

    print("\n=== Mock Demo ===")
    mock = SimpleMock()
    mock.when_called_with("hello").then_return("HELLO")
    mock.when_called_with("world").then_return("WORLD")

    print(f"'hello' -> {mock('hello')}")
    print(f"'world' -> {mock('world')}")

    print("\n=== Assertion Functions Demo ===")
    assert_equal("a" + "b", "ab")
    assert_true(1 < 2)
    assert_false([])

    def raise_error():
        raise ValueError("test error")

    assert_raises(ValueError, raise_error)
    print("All assertions passed")

    print("\nDemo OK")


if __name__ == "__main__":
    demo()