import json
import os
from typing import Optional, Literal

from app import JsonData


def json_wr(
    filename: str,
    mode: Literal["r", "w"] = "r",
    data: Optional[JsonData] = {}
) -> Optional[JsonData]:
    """Write and read json files.

    Parameters
    ----------
    filename : str
        Name of the file. It opens the file like "app/" + filename + ".json".
    mode : "r", "w", default="r"
        Action to perform in the file.
        "r" to load data, "w" to write in the file.
    data : JsonData, optional, default={}
        Data to write in the file if you're in "w" mode.

    Returns
    -------
    JsonData, optional
        Data of the file or default one if the mode is "r".
        Nothing if the mode is "w".
    """
    filename = f"app/{filename}.json"

    if mode == "r":
        if not os.path.isfile(filename):
            return data
        with open(filename) as f:
            return json.load(f)

    elif mode == "w":
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    return
