import inspect
from parsers.converter import serialize, deserialize


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

    classes = (class1, class2, class3)
    for cls in classes:
        assert obj_to_dict(deserialize(serialize(cls))) == obj_to_dict(cls)

