from parsers.json_parser.dump import obj_to_str # pragma: no cover
from parsers.json_parser.load import str_to_obj # pragma: no cover
from parsers.serializer_creator.parser_interface import Parser # pragma: no cover


class JsonParser(Parser): # pragma: no cover
    def dump(self, obj, fp):
        fp.write(obj_to_str(obj))

    def dumps(self, obj) -> str:
        return obj_to_str(obj)

    def load(self, fp):
        doc = fp.read()
        if doc == '':
            return ''
        return str_to_obj(doc)

    def loads(self, s):
        if s == '':
            return ''
        return str_to_obj(s)


# a = 123
# def f():
#     print(a)
#
# print(JsonParser().dumps(f))