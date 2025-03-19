import os
import subprocess
import argparse
import uuid


class FileHelper:
    """
    FileHelper handles all operations file related.
    Every operation is first done on either a copy of the existing
    service in a local temp file, or in a new temp file.
    After the file is written, the file is moved into the systemd
    service directory.
    """

    def _overwrite(self, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write('')

    def _service_exists(self, filename: str) -> bool:
        return os.path.isfile(f"/etc/systemd/system/{filename}.service")
    
    def _make_tmp_copy(self, filename: str) -> str:
        tmp_name = str(uuid.uuid1())
        cpy_process = subprocess.run(f"sudo cp /etc/systemd/system/{filename} {tmp_name}", shell=True, text=True, capture_output=True)
        print(cpy_process.stderr)
        if cpy_process.stderr:
            raise Exception(f"Couldn't make a safe copy of {filename}: {cpy_process.stderr}")
        return tmp_name

    def _make_tmp(self, filename: str) -> str:
        tmp_name = str(uuid.uuid1())
        touch_process = subprocess.run(f"touch {tmp_name}", shell=True, text=True, capture_output=True)
        if touch_process.stderr:
            os.system(f"rm {tmp_fn}")
            raise Exception(f"Couldn't make safe file for {filename}: {touch_process.stderr}")
        return tmp_name

    def _merge(self, tmp_name: str, filename: str) -> None:
        mv_process = subprocess.run(f"sudo mv {tmp_name} /etc/systemd/system/{filename}", shell=True, text=True, capture_output=True)
        if mv_process.stderr:
            os.system(f"rm {tmp_fn}")
            raise Exception(f"Couldn't merge {tmp_name} into {filename}")
    
    def _write_sections(self, tmp_fn: str, ordered_args: dict) -> None:
        print("writing ...")
        with open(tmp_fn, 'a+') as f:
            for section in ['Unit', 'Service', 'Install']:
                f.write(f"[{section}]\n")
                for line in ordered_args[section]:
                    f.write(line + '\n')

    def create(self, fn: str, ordered_args: dict) -> None:
        tmp_fn = self._make_tmp(fn)
        self._overwrite(tmp_fn)
        self._write_sections(tmp_fn, ordered_args)
        self._merge(tmp_fn, fn)

