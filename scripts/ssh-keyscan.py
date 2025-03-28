import os
import subprocess as sp
import sys
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


def load_inventory(fpath: str | os.PathLike[str] = "inventory.yaml") -> Any:
    fpath = Path(fpath)
    yaml = YAML()
    with fpath.open("r") as fp:
        return yaml.load(fp)


def ssh_keyscan(host: str, port: int | None = None, *, hash: bool = True) -> str:
    args: list[str] = ["ssh-keyscan"]
    if port is not None:
        args += ["-p", str(port)]
    if hash:
        args += ["-H"]
    args += [host]
    proc: sp.CompletedProcess[str] = sp.run(args, stdout=sp.PIPE, check=True, text=True)
    return proc.stdout


def main() -> None:
    inventory: Any = load_inventory()
    for hosts_name, values in inventory.items():
        hosts = values["hosts"]
        for host, values in hosts.items():
            host = values["ansible_host"]
            port = values.get("ansible_port")
            try:
                keys: str = ssh_keyscan(host, port)
            except sp.CalledProcessError as e:
                print(f"Error: {e}", file=sys.stderr)
            else:
                print(keys)


if __name__ == "__main__":
    main()
