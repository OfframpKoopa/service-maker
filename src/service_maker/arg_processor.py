"""
    The arg_processor module allows operations relative to the formatting
    of the arguments namespace object.
    It is only responsible for processing the data in a way
    that is useful for writing it or checking it.
    It does not modify the data, nor makes state change in the
    main process.
"""

import argparse
import attr


# validators.directives.key
class Validators:
    """ 
    This class serves as a namespace for the model validators.
    You can use it this way : 
        validators = Validators()
        validators.directives.key 
            -> Returns the key validators for directives
    """
    class directives:
        
        @staticmethod
        def key(value):
        """ directives should only have str keys. """
        if not isinstance(value, str):
            raise ValueError(f"{value} is not a valid key for a Directives object")

        @staticmethod
        def value(value):
            """ directives value should be none or a list """
            if value is not None and not isinstance(value, list):
                raise ValueError(f"{value} is not a valid value for a Directives object")

    class sections:

        @staticmethod
        def key(value):
            """"""
            pass

        @staticmethod
        def value(value):
            """"""
            pass

    class raw_service:

        @staticmethod
        def key(value):
            pass

        @staticmethod
        def value(value):
            pass


@attr.s(frozen=True)
class Directives(dict):
    validators = Validators()

    directives = attr.ib(
            validator=attr.validators.deep_mapping(
                key_validator=validators.directives.key,
                value_validator=validators.directives.value)
            )

    def __attrs_post_init__(self):
        super().__init__(self.directives)

    def __setitem__(self, key, value):
        raise TypeError("Cannot edit an immutable object.")

    def __delitem__(self, key):
        raise TypeError("Cannot edit an immutable object.")

    def __getitem__(self, key):
        return super().__getitem__(key)


@attr.s(frozen=true)
class sections(dict):
    validators = validators()

    sections = attr.ib(
            validator=attr.validators.deep_mapping(
                key_validator=validators.sections.key,
                value_validator=validators.sections.value)
            )

   def __attrs_post_init__(self):
        super().__init__(self.sections)

    def __setitem__(self, key, value):
        raise TypeError("cannot edit an immutable object.")

    def __delitem__(self, key):
        raise TypeError("cannot edit an immutable object.")

    def __getitem__(self, key):
        return super().__getitem__(key)



@attr.s(frozen=True)
class RawService(list):
    raw_service_data = attr.ib()

    def __getitem__(self, key):
        return super().__getitem__(key)

@attr.s(frozen=true)
class RawService(list):
    validators = validators()

    raw_service = attr.ib(
            validator=attr.validators.deep_mapping(
                key_validator=validators.raw_service.key,
                value_validator=validators.raw_service.value)
            )

   def __attrs_post_init__(self):
        super().__init__(self.sections)



class Converter(ABC):
    """ Interface to implement converters  """

    @abstractmethod
    def to_dict(self):
        raise NotImplementedError("Can't convert to this type.")

    @abstractmethod
    def to_ordered(self):
        raise NotImplementedError("Can't convert to this type.")

    @abstractmethod
    def to_raw(self):
        raise NotImplementedError("Can't convert to this type.")


class DirectivesConverter(Converter):
    """ Handles conversion operations for Dict source. """
    def __init__(directives: Directives, doc_reference: dict) -> None:
        self.directives = directives
        self.doc_reference = doc_reference


class SectionsConverter(Converter):
    """ Handles conversion operations for Ordered source. """
    def __init__(sections: Sections, doc_reference: dict) -> None:
        self.sections = sections
        self.doc_reference = doc_reference


class RawServiceConverter(Converter):
    """ Handles conversion operations for Raw source. """
    def __init__(raw_service: RawService, doc_reference: dict) -> None:
        self.raw_service = raw_service
        self.doc_reference = doc_reference


def parse_raw_section(raw_section: str) -> str:
    section = raw_section.strip("[")
    section = section.strip("]\n")
    return section

def parse_raw_directive(raw_directive: str) -> list:
    directive = raw_directive.split("=")
    directive[0] = directive[0].strip("# ")
    directive[1] = directive[1].strip("\n")
    directive[1] = None if not directive[1] else [directive[1]]
    return directive

def by_raw_list(raw_args: list) -> dict:
    """ Reverse the parsing process from raw files to ordered dict """
    ordered_args = {}
    current_section = ""
    for line in raw_args:
        if line.startswith("["):
            continue
        directive = parse_raw_directive(line)
        ordered_args[directive[0]] = directive[1]
    return ordered_args

def update_ordered_args(args: dict, updated_args: dict) -> dict:
    args.update(updated_args)
    return args

def by_section(name: str,
               data_dict: dict,
                section: str,
                defaulting: bool = True,
                enabled: bool = True) -> list:
    """
    Returns a list of directives associated with the section
    argument passed.

    defaulting : fills some empty fields with default datas.
    enabled : fills WantedBy directive so service can be enabled.
    """
    if not section:
        return []

    datas = data_dict
    section_directives = []
    for parameter in datas.get(section, []):
        directive = []
        if defaulting:
            value = _default_data(name, args, parameter, enabled)
        if not value:
            directive.append("# ")
        directive.append(parameter)
        directive.append('=')
        if value:
            directive.append(''.join(value))
        section_directives.append(''.join(directive))
    return section_directives

def _default_data(name: str,
                  args: dict,
                  parameter: str,
                  enabled: bool) -> str:
    """ Check that the parameter without a value assigned
        has to be defaulted or not.
        'enabled' means WantedBy field needs default value so
        the service can be enabled by systemctl.
    """
    value = args.get(parameter, "")
    if value:
        return value

    if parameter == "Alias":
        value = name + ".service"
    if parameter == "Description":
        value = f"{name} is a service-maker generated service."

    # Enabled fills fields needed for service enabling
    if parameter == "WantedBy" and enabled:
        value = "multi-user.target"

    return value

