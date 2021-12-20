import json
import os
from typing import Optional, List, Dict, Union

from app import JsonData


def json_wr(
    path: str,
    mode: str = "r",
    data: Optional[JsonData] = {}
) -> Optional[JsonData]:
    """
    Read json data or write given data with given file path.

    file_path: path of the file to write inside
    data: data to write inside the file (optional)
    if_none: if you're trying to read the file and it does not exist
             it will return this
    """
    path = f"app/{path}.json"

    if mode == "w":
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
            return

    elif mode == "r":
        if not os.path.isfile(path):
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
        with open(path) as f:
            return json.load(f)
