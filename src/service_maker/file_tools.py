import os
import subprocess
import argparse
import uuid


def service_exists(filename: str) -> bool:
    """ check if service exists. (Unexpected, I know.)"""
    return os.path.isfile(f"{filename}")

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
    """ Manage operations with the service file.
        Every operation is done on a safe temporary file.
        Use the merge() method to save the service file in
        /etc/systemd/system/

        FileManager should be agnostic to the models custom
        types. 
        
        - For writing, we assume that the data is exactly how 
        we should write it.
        
        - Same when reading, we should get the rawest input
        to start the parsing process.
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename + ".service"
        self.tmp_name = str(uuid.uuid1())
        self.service_dir = "/etc/systemd/system/"

    def create_tmp(self) -> None:
        """ create empty tmp file. """
        with open(self.tmp_name, 'w') as f:
            f.write("")

    def write(self, line: str) -> None:
        """ write content inside tmp file """
        with open(self.tmp_name, "a") as f:
            f.write(line + "\n")

    def writelines(self, lines: list) -> None:
        with open(self.tmp_name, "w") as f:
            f.writelines(lines)

    def read(self) -> list:
        """ read the current filename and returns its content
            as a list
        """
        service_full_path = self.service_dir + self.filename
        if not service_exists(service_full_path):
            raise Exception(f"{self.filename} does not exists.")
        
        with open(service_full_path, "r") as f:
            return f.readlines()

    def commit(self) -> None:
        """ overwrite systemd file (if exists else just moves
        the tmp file) with temp file. """
        cmd = f"sudo mv {self.tmp_name} /etc/systemd/system/{self.filename}"
        result = subprocess.run(cmd,
                                shell=True,
                                text=True,
                                capture_output=True)
        if result.stderr:
            raise RuntimeError(f"Couldn't mv temp file {self.tmp_name}: {result.stderr}")

