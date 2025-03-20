"""
    The arg_processor module allows operations relative to the formatting
    of the arguments namespace object.
    It is only responsible for processing the data in a way
    that is useful for writing it or checking it.
    It does not modify the data, nor makes state change in the
    main process.
"""

import argparse


def by_section(arg_np: argparse.Namespace,
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

    datas = getattr(arg_np, "datas", {})
    args = vars(arg_np)
    section_directives = []
    for parameter in datas.get(section, []):
        directive = []
        if defaulting:
            value = _default_data(arg_np, args, parameter, enabled)
        if not value:
            directive.append("# ")
        directive.append(parameter)
        directive.append('=')
        if value:
            directive.append(''.join(value))
        section_directives.append(''.join(directive))
    return section_directives


def _default_data(arg_np: argparse.Namespace,
                  args: dict,
                  parameter: str,
                  enabled: bool) -> str:
    """ Check that the parameter without a value assigned
        has to be defaulted or not.
        'enabled' means WantedBy field needs default value so
        the service can be enabled by systemctl.
    """
    value = args.get(parameter, "")
    name = getattr(arg_np, "Name", [""])[0]
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
