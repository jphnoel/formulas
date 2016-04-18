from unittest import TestCase
from sys import modules
import inspect


def currying(elem):
    def func_decorator(func):
        def func_wrapper(self):
            return func(self, elem)
        return func_wrapper
    return func_decorator


def to_tesst(func):
    func.__to_test__ = 1
    return func


def retrieve_test_methods(klass):
    methods = inspect.getmembers(klass, predicate=inspect.ismethod)
    return [m[1] for m in methods if hasattr(m[1], '__to_test__')]


def class_dec(testable_list):
    def class_decorator(klass):
        test_methods = retrieve_test_methods(klass)
        for testable_obj in testable_list:
            attrs = {}
            for m in test_methods:
                for i, rule in enumerate(testable_obj):
                    decorated_m = currying(rule)(m)
                    decorated_m.__test__ = 1
                    test_name = "Test_%s_on_testable_obj_%d" % (m.__name__, i + 1)
                    attrs[test_name] = decorated_m

            tl_test_klass = type("test_%s" % testable_obj.name, (klass,), attrs)
            setattr(modules[klass.__module__], tl_test_klass.__name__,
                    tl_test_klass)
    return class_decorator