from parsers.serializer_creator import AbstractSerializerCreator
from parsers.pickle_parser.parser import PickleParser
from parsers.serializer_creator.parser_interface import Parser


class PickleSerializerCreator(AbstractSerializerCreator):
    def create_serializer(self) -> Parser:
        return PickleParser()
