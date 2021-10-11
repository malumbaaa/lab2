from parsers.serializer_creator import AbstractSerializerCreator
from parsers.toml_parser.parser import TomlParser
from parsers.serializer_creator.parser_interface import Parser


class TomlSerializerCreator(AbstractSerializerCreator):
    def create_serializer(self) -> Parser:
        return TomlParser()
