import inspect
import types
from codecs import encode
from parsers.json_parser.tokens import *


def str_to_obj(doc):
    tokens = doc_to_tokens(doc)
    obj = _tokens_to_obj(tokens)
    _bind_methods(obj)
    return obj


def _bind_methods(obj): # pragma: no cover
    funcs = dict(inspect.getmembers(obj, inspect.isfunction))

    for name in funcs:
        args = list(inspect.signature(funcs[name]).parameters)
        funcs[name].__name__ = name
        if len(args) > 0 and args[0] == 'self':
            bound_method = funcs[name].__get__(obj, obj.__class__)
            setattr(obj, name, bound_method)

    for name, val in inspect.getmembers(obj):
        if inspect.isclass(val) and not name.startswith('__'):
            _bind_methods(val)


def _tokens_to_obj(tokens):
    parsers = (_parse_function, _parse_class, _parse_object, _parse_dict, _parse_array)

    d = dict(zip(flags + ('{', '['), parsers))

    if tokens[0] in d:
        return d[tokens.pop(0)](tokens)

    return tokens.pop(0)


def _dict_to_obj(d, name):
    if not isinstance(d, dict):
        return d

    obj = type(name, (), {})
    obj = obj()

    for key in d:
        obj.__dict__[key] = d[key]

    return obj


def _parse_object(tokens):
    name = tokens.pop(0)
    tokens.pop(0)
    obj_dict = _parse_dict(tokens)
    return _dict_to_obj(obj_dict, name)


def _parse_class(tokens):
    name = tokens.pop(0)
    d = {}
    source = tokens[0].strip()
    tokens.pop(0)
    exec(source, d)
    return d[name]


def __make_cell():
    if False:
        cell = None
    return (lambda: cell).__closure__[0]


def _parse_function(tokens):
    name = tokens.pop(0)
    tokens.pop(0)
    d = _parse_dict(tokens)

    co: types.CodeType = compile(d['source'].strip(), '<string>', 'exec')
    co = co.co_consts[0]
    co_freevars = tuple(d['closure'].keys())
    co_names = tuple([e for e in co.co_names if e not in d['closure']])
    co_code = d['byte_code']
    co_code = encode(co_code, "raw_unicode_escape")
    co = co.replace(co_freevars=co_freevars, co_name=name, co_names=co_names, co_code=co_code)

    gl = dict(**d['globals'], **{'__builtins__': __builtins__})

    closure = []
    for k in d['closure']:
        cell = __make_cell()
        cell.cell_contents = d['closure'][k]
        closure.append(cell)

    func = types.FunctionType(code=co, globals=gl, closure=tuple(closure))
    return func


def _parse_function2(tokens):# pragma: no cover
    def f():
        pass

    name = tokens.pop(0)
    tokens.pop(0)
    d = _parse_dict(tokens)

    co_freevars = tuple(d['closure'].keys())
    co_names = tuple(d['names'])
    co_code = d['byte_code']
    co_code = encode(co_code, "raw_unicode_escape")
    co = f.__code__
    co = co.replace(co_freevars=co_freevars, co_name=name, co_names=co_names, co_code=co_code)

    gl = dict(**d['globals'], **{'__builtins__': __builtins__})

    closure = []
    for k in d['closure']:
        cell = __make_cell()
        cell.cell_contents = d['closure'][k]
        closure.append(cell)

    func = types.FunctionType(code=co, globals=gl, closure=tuple(closure))
    return func


def _parse_dict(tokens):
    _object = {}

    if tokens[0] == '}':
        tokens.pop(0)
        return _object

    while True:
        key = tokens.pop(0)

        if tokens.pop(0) != ':':
            raise Exception()

        val = _tokens_to_obj(tokens)
        _object[key] = val

        token = tokens.pop(0)
        if token == '}':
            return _object
        if token != ',':
            raise Exception()


def _parse_array(tokens):
    _array = []

    if tokens[0] == ']':
        tokens.pop(0)
        return _array

    while True:
        val = _tokens_to_obj(tokens)
        _array.append(val)

        token = tokens.pop(0)
        if token == ']':
            return _array
        if token != ',':
            raise Exception()
