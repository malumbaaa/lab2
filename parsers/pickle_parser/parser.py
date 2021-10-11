import pickle
from parsers.serializer_creator.parser_interface import Parser
from parsers.converter import serialize, deserialize


class PickleParser(Parser):
    def dump(self, obj, fp):
        pickle.dump(serialize(obj), fp)

    def dumps(self, obj):
        return pickle.dumps(serialize(obj))

    def load(self, fp):
        return deserialize(pickle.load(fp))

    def loads(self, s):
        return deserialize(pickle.loads(s))
