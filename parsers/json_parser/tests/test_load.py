import math
import inspect
from parsers.json_parser.dump import obj_to_str
from parsers.json_parser.load import str_to_obj


def test_kk():
    assert str_to_obj(obj_to_str(['foo', {'bar': ('baz', None, 1.0, 2)}])) == ['foo', {'bar': ['baz', None, 1.0, 2]}]


def test_simple_type():
    items = (0, -1, 545453486545, '', -float('inf'), float('inf'), -121.46, -4654e-10, False, True,
             'fg', 'None', "1.65", -65, 1e10)
    for item in items:
        assert str_to_obj(obj_to_str(item)) == item
    assert str_to_obj(obj_to_str('\n')) == '\n'
    assert math.isnan(str_to_obj(obj_to_str(float('nan'))))


def test_array():
    items = ([], [[[]]], list(), [4], [[[True], -2], '3'], [1, [2.54, [3e-10]]], [[''], ""])
    for item in items:
        assert str_to_obj(obj_to_str(item)) == item


def test_dict():
    items = [{}, {'a': {'b': {'c': 1}}}, dict(g=1), {'': 1}, {'': {'g': {'a': -1}, 'b': -14e-10}, 'c': ''}, {'1': 1}]
    for item in items:
        assert str_to_obj(obj_to_str(item)) == item


b = 66
def test_func():
    def f1():
        return 1 + 3
    a = 4
    def f2():
        return a + b
    f3 = lambda: a + b

    to_remove = (' ', '\n', '\t')
    functions = (f1, f2, f3)
    for func in functions:
        assert str_to_obj(obj_to_str(func))() == func()


class class1():
    pass

class class2():
    b = 1
    class a(object):
        k = [[2], 2, 2]
        def f(self):
            print('1')

class class3(object):
    a = None
    b = [1, (1, 5)]
    c = False
    d = "gds"
    e = {"a": 11, "b": {1: 21, 2: 22}}


def obj_to_dict(odj):
    d = {}
    for key, val in inspect.getmembers(odj):
        if key.startswith('__'):
            continue
        if inspect.isfunction(val) or inspect.ismethod(val):
            d[key] = 'func'
        elif inspect.isclass(val):
            d[key] = obj_to_dict(val)
        else:
            d[key] = val
    return d

def test_class():
    classes = (class1, class2, class3)
    attr = []
    for cls in classes:
        assert obj_to_dict(str_to_obj(obj_to_str(cls))) == obj_to_dict(cls)
    str_to_obj(obj_to_str(class2)).a.f()

class abc(object):
    a = None
    b = [1, (1, 5)]
    c = False
    d = "gds"
    e = {"a": 11, "b": {1: 21, 2: 22}}

    def f(self, s, k):
        v = 1 + 2 + s - k
        return v

    class gg():
        a = None
        b = [1, (1, 5)]
        c = False
        d = 'gds'
def test_object():
    classes = (class1, class2, class3, abc)
    for cls in classes:
        cls_object = cls()
        assert obj_to_dict(str_to_obj(obj_to_str(cls))) == obj_to_dict(cls_object)
