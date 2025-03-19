import argparse
from service_maker.commands import Command, Create, Update


class CommandInvoker:
    def __init__(self, db: dict) -> None:
        self.db = db
        self.arg_parser = argparse.ArgumentParser()
        self._register_arguments()

    def _register_arguments(self) -> None:
        """ argparse specifig implementation. """
        for section, params in self.db.items():
            for param in params:
                self.arg_parser.add_argument("--" + param, action="append")
        self.arg_parser.add_argument("action", choices=["create", "update"])

    def get_command(self) -> Command:
        """ return a Command object related to the action argument. """
        arg_np = self.arg_parser.parse_args()
        arg_np.sections = list(self.db.keys())
        arg_np.datas = self.db

        if arg_np.action == "create":
            command = Create(arg_np)

        if arg_np.action == "update":
            command = Update(arg_np)

        if not command:
            raise Exception(f"Command {arg_np.action} unexpectedly failed.")
        return command

