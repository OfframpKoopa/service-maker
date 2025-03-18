import json
import os

from service_maker.command_invoker import CommandInvoker
from service_maker.commands import Command # for typing


base_path = os.path.dirname(__file__)
db_path = os.path.join(base_path, 'db.json')

def build_db(filename: str = db_path ) -> dict:
    with open(filename, 'r') as f:
        db = json.load(f)
    return db


def main() -> None:
    db = build_db()
    invoker = CommandInvoker(db)
    command = invoker.get_command()

    try:
        command.execute()
        print(f"{command.arg_np.Name} successfully created/updated.")
    except Exception as e:
        print(f"[error] ServiceMaker encountered following issu: {e}")


if __name__ == '__main__':
    main()
