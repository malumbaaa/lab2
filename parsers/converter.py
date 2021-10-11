import dis
import inspect
import opcode
import types
from codecs import encode

_simple_type = (str, bool, int, float)
function_flag = '_func'
class_flag = '_class'
object_flag = '_object'


GLOBAL_OPS = (opcode.opmap['STORE_GLOBAL'], opcode.opmap['DELETE_GLOBAL'], opcode.opmap['LOAD_GLOBAL'])


def _walk_global_ops(code):
    for instr in dis.get_instructions(code):
        op = instr.opcode
        if op in GLOBAL_OPS:
            yield op, instr.arg


def function_to_dict(func):
    _source = inspect.getsource(func).replace('"', '\"').replace("'", '\'')
    co = func.__code__
    names = co.co_names
    _globals = {names[oparg] for _, oparg in _walk_global_ops(co)}
    _globals = {k: func.__globals__[k] for k in _globals if k in func.__globals__}
    _closure = dict()
    if func.__closure__ is not None:
        _closure = dict((co.co_freevars[i], c.cell_contents) for i, c in enumerate(func.__closure__))

    _names = tuple([e for e in co.co_names if e not in _closure.keys()])
    _code = str(co.co_code)[2:-1].encode().decode('unicode_escape')

    return {"source": _source, "globals": _globals, "closure": _closure, "byte_code": _code}


def serialize(obj):
    if type(obj) in _simple_type:
        return obj
    elif type(obj) is dict:
        for k in obj:
            obj[k] = serialize(obj[k])
        return obj
    elif isinstance(obj, list) or isinstance(obj, tuple):
        l = []
        for o in obj:
            l.append(serialize(o))
        return l
    elif inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, types.LambdaType):
        return {function_flag: {obj.__name__: function_to_dict(obj)}}
    elif inspect.isclass(obj):
        return {class_flag: {obj.__name__: inspect.getsource(obj).strip()}}
    elif hasattr(obj, '__dict__'):
        tmp = {}
        d = {object_flag: {type(obj).__name__: tmp}}
        for a in dir(obj):
            if a.startswith('__'):
                continue
            val = getattr(obj, a)
            if type(val) in _simple_type:
                tmp[a] = val
            else:
                tmp[a] = serialize(val)
        return d


def _make_cell():
    if False:
        cell = None
    return (lambda: cell).__closure__[0]


def dict_to_function(d):
    name = list(d.keys())[0]
    d = d[name]
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
        cell = _make_cell()
        cell.cell_contents = d['closure'][k]
        closure.append(cell)

    func = types.FunctionType(code=co, globals=gl, closure=tuple(closure))
    return func


def deserialize(obj):
    if type(obj) in _simple_type:
        return obj
    elif isinstance(obj, list) or isinstance(obj, tuple):
        l = []
        for o in obj:
            l.append(deserialize(o))
        return l
    elif isinstance(obj, dict):
        for key, val in obj.items():
            if key == function_flag:
                return dict_to_function(val)
            if key == class_flag:
                return inspect.getsource(val)
            elif key == object_flag:
                items = val.items()
                name, d = list(items)[0]
                o = type(name, (), {})
                o = o()
                for k in d:
                    o.__dict__[k] = deserialize(d[k])
                return o
            elif type(val) in _simple_type:
                pass
            elif isinstance(val, list) or isinstance(val, tuple):
                l = []
                for o in val:
                    l.append(deserialize(o))
                obj[key] = l
            return obj

