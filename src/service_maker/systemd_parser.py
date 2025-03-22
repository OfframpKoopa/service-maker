from abc import ABC, abstractmethod

from .models import Directives, Sections, RawService


class Converter(ABC):
    """ Interface to implement converters  """

    @abstractmethod
    def to_directives(self):
        raise NotImplementedError("Can't convert to this type.")

    @abstractmethod
    def to_sections(self):
        raise NotImplementedError("Can't convert to this type.")

    @abstractmethod
    def to_raw_service(self):
        raise NotImplementedError("Can't convert to this type.")


class DirectivesConverter(Converter):
    """ Handles conversion operations for Dict source. """
    def __init__(directives: Directives, doc_reference: dict) -> None:
        self.directives = directives
        self.doc_reference = doc_reference

    def to_directives(self) -> Directives:
        return self.directives
    
    def to_sections(self) -> Sections:
        pass

    def to_raw_service(self) -> RawService:
        pass


class SectionsConverter(Converter):
    """ Handles conversion operations for Ordered source. """
    def __init__(sections: Sections, doc_reference: dict) -> None:
        self.sections = sections
        self.doc_reference = doc_reference

    def to_directives(self) -> Directives:
        pass

    def to_sections(self) -> Sections:
        return self.sections

    def to_raw_service(self) -> RawService:
        pass


class RawServiceConverter(Converter):
    """ Handles conversion operations for Raw source. """
    def __init__(raw_service: RawService, doc_reference: dict) -> None:
        self.raw_service = raw_service
        self.doc_reference = doc_reference

    def to_directives(self) -> Directives:
        pass

    def to_sections(self) -> Sections:
        pass

    def to_raw_service(self) -> RawService:
        return self.raw_service


