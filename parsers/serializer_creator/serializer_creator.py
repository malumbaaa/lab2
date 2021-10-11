from parsers.serializer_creator import JsonSerializerCreator
from parsers.serializer_creator.pickle_serializer_creator import PickleSerializerCreator
from parsers.serializer_creator import TomlSerializerCreator
from parsers.serializer_creator.yaml_serializer_creator import YamlSerializerCreator


def create_serializer(serializer: str):
    if serializer.upper() == 'JSON':
        return JsonSerializerCreator().create_serializer()
    if serializer.upper() == 'TOML':
        return TomlSerializerCreator().create_serializer()
    if serializer.upper() == 'YAML':
        return YamlSerializerCreator().create_serializer()
    if serializer.upper() == 'PICKLE':
        return PickleSerializerCreator().create_serializer()
