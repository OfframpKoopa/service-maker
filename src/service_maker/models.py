import attr

from .validators import Validators


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


@attr.s(frozen=True)
class Sections(dict):
    validators = Validators()

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
    validators = Validators()

    raw_service = attr.ib(
            validator=attr.validators.deep_iterable(
                member_validator=validators.raw_service.value,
                iterable_validator=attr.validators.instance_of(list))
            )

    def __attrs_post_init__(self):
        super().__init__(self.raw_service)

