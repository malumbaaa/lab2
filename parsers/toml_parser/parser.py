import pytomlpp
from parsers.serializer_creator.parser_interface import Parser
from parsers.converter import serialize, deserialize


class TomlParser(Parser):
    def dump(self, obj, fp):
        pytomlpp.dump(serialize(obj), fp)

    def dumps(self, obj) -> str:
        return pytomlpp.dumps(serialize(obj))

    def load(self, fp):
        return deserialize(pytomlpp.load(fp))

    def loads(self, s):
        return deserialize(pytomlpp.loads(s))
