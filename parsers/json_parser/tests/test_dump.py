import json
import inspect
from parsers.json_parser.dump import obj_to_str


def test_kk():
    assert obj_to_str(['foo', {'bar': ('baz', None, 1.0, 2)}]) == json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])


def test_simple_type():
    items = (0, -1, 545453486545, '', -float('inf'), float('inf'), float('nan'), -121.46, -4654e-10, False, True,
             'fg', 'None', "1.65", -65)
    for item in items:
        assert obj_to_str(item) == json.dumps(item)
    assert obj_to_str('\\n') == json.dumps('\n')


def test_array():
    items = ([], [[[]]], list(), (), (()), [4], [[[True], -2], '3'], [1, [2.54, [3e-10]]], [(''), ""])
    for item in items:
        assert obj_to_str(item) == json.dumps(item)


def test_dict():
    items = [{}, {'a': {'b': {'c': 1}}}, dict(g=1), {'': 1}, {'': {'g': {'a': -1}, 'b': -14e-10}, 'c': ''}, {1: 1}]
    for item in items:
        assert obj_to_str(item) == json.dumps(item)


a = 123
def test_func():
    def f1():
        pass

    def f2(self):
        print(self)

    def f3(a=[]):
        pass

    f4 = lambda x, y: x + y
    b = 333
    f5 = lambda: print(a+b)
    to_remove = (' ', '\n', '\t')
    functions = (f1, f2, f3, f4)
    for func in functions:
        bytes = str(func.__code__.co_code)[2:-1].encode().decode('unicode_escape')
        assert obj_to_str(func) == \
               f'function("{func.__name__}"): ' \
               f'{{"source": "{inspect.getsource(func)}", ' \
               f'"globals": {{}}, "closure": {{}}, "byte_code": "{bytes}"}}'
    bytes = str(f5.__code__.co_code)[2:-1].encode().decode('unicode_escape')
    print(obj_to_str(f5))
    assert obj_to_str(f5) == \
               f'function("{f5.__name__}"): {{"source": "{inspect.getsource(f5)}", ' \
               f'"globals": {{"a": 123}}, "closure": {{"b": 333}}, "byte_code": "{bytes}"}}'


class class1():
    pass
class class2(class1):
    b = 1
    class a():
        def f(self):
            print('1')
        pass
class class3(object):
    a = None
    b = [1, (1, 5)]
    c = False
    d = "gds"
    e = {"a": 11, "b": {1: 21, 2: 22}}


def test_class():
    classes = (class1, class2, class3)
    for cls in classes:
        source = inspect.getsource(cls).replace('"', r'\"').replace("'", r'\'')
        assert obj_to_str(cls) == \
               f'class("{cls.__name__}"): "{source}"'


def test_object():
    classes = (class1, class3)
    for cls in classes:
        cls_object = cls()
        attr = dict([(key, val) for key, val in inspect.getmembers(cls_object) if not key.startswith('__')])
        assert obj_to_str(cls_object) == \
           f'object("{type(cls_object).__name__}"): {json.dumps(attr)}'
