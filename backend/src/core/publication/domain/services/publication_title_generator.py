from abc import ABC, abstractmethod


class PublicationTitleGenerator(ABC):

    @abstractmethod
    def generate(
        content: str
    ) -> str:
        pass
