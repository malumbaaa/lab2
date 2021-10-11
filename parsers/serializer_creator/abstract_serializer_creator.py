from abc import abstractmethod


class AbstractSerializerCreator:
    @abstractmethod
    def create_serializer(self):
        pass
