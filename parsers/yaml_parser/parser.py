import yaml
from parsers.serializer_creator.parser_interface import Parser
from parsers.converter import serialize, deserialize


class YamlParser(Parser):
    def dump(self, obj, fp):
        yaml.dump(serialize(obj), fp)

    def dumps(self, obj) -> str:
        return yaml.dump(serialize(obj))

    def load(self, fp):
        return deserialize(yaml.safe_load(fp))

    def loads(self, s):
        return deserialize(yaml.safe_load(s))
