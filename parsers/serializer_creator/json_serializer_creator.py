from parsers.serializer_creator import AbstractSerializerCreator
from parsers.json_parser.parser import JsonParser
from parsers.serializer_creator.parser_interface import Parser


class JsonSerializerCreator(AbstractSerializerCreator):
    def create_serializer(self) -> Parser:
        return JsonParser()
