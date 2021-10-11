from enum import Enum
from parsers.serializer_creator.serializer_creator import create_serializer


class ParsersEnum(Enum):
    JSON = 'Json'
    YAML = 'Yaml'
    TOML = 'Toml'
    PICKLE = 'Pickle'


def convert(deserializer, serializer, file_to_convert, file_to_save=None):
    if not isinstance(deserializer, ParsersEnum):
        raise TypeError('serializer must be an instance of ParsersEnum')
    if not isinstance(serializer, ParsersEnum):
        raise TypeError('deserializer must be an instance of ParsersEnum')

    if deserializer == serializer:
        return

    if deserializer == ParsersEnum.PICKLE:
        file_to_convert = open(file_to_convert, 'rb')
    else:
        file_to_convert = open(file_to_convert, 'r')
    if file_to_save is not None:
        if serializer == ParsersEnum.PICKLE:
            file_to_save = open(file_to_save, 'w')
        else:
            file_to_save = open(file_to_save, 'wb')

    deserializer_obj = create_serializer(deserializer.value)
    obj = deserializer_obj.load(file_to_convert)
    file_name = file_to_convert.name
    file_to_convert.close()

    serializer_obj = create_serializer(serializer.value)
    if file_to_save is None:
        if serializer == ParsersEnum.PICKLE:
            file_to_save = open(file_name, 'wb')
        else:
            file_to_save = open(file_name, 'w')
    serializer_obj.dump(obj, file_to_save)
    file_to_save.close()

