import os
import subprocess
import argparse
import uuid


def service_exists(filename: str) -> bool:
    """ check if service exists. (Unexpected, I know.)"""
    return os.path.isfile(f"/etc/systemd/system/{filename}")

def copy_service(filename: str, tmp_name: str) -> None:
    """ copy service file content into temporary service file. """
    cmd = f"sudo cp /etc/systemd/system/{filename} {tmp_name}"
    result = subprocess.run(cmd,
                            shell=True,
                            text=True,
                            capture_output=True)
    if result.stderr:
        raise RuntimeError(f"Erreur lors de la copie : {result.stderr}")


class FileManager:
    """ Manage creation and writing of the service file.
        Every operation is done on a safe temporary file.
        Use the merge() method to save the service file in
        /etc/systemd/system/
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename + ".service"
        self.tmp_name = str(uuid.uuid1())

    def create_tmp(self) -> None:
        """ create empty tmp file. """
        with open(self.tmp_name, 'w') as f:
            f.write("")

    def write(self, line: str) -> None:
        """ write content inside tmp file """
        with open(self.tmp_name, "a") as f:
            f.write(line + "\n")

    def merge(self) -> None:
        """ overwrite systemd file (if exists else just moves
        the tmp file) with temp file. """
        cmd = f"sudo mv {self.tmp_name} /etc/systemd/system/{self.filename}"
        result = subprocess.run(cmd,
                                shell=True,
                                text=True,
                                capture_output=True)
        if result.stderr:
            raise RuntimeError(f"Erreur lors du déplacement du fichier : {result.stderr}")

