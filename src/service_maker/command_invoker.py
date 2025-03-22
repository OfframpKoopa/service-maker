""" module to handle Commands creation, supervision and exception. """

from service_maker.commands import Command, Create, Update


def get_command(action: str) -> Command:
    """ return a Command object related to the action argument. """
    command = ""

    if action == "create":
        command = Create()

    if action == "update":
        command = Update()

    if not command:
        raise Exception(f"Command {action} unexpectedly failed.")

    return command

