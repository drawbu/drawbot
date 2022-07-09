import json
import os
from typing import Dict, Any, List, Union, Optional, Literal

JsonDict = Dict[str, Any]
JsonList = List[Any]
JsonData = Union[JsonDict, JsonList]


def json_wr(
    filename: str, mode: Literal["r", "w"] = "r", data=None
) -> Optional[JsonData]:
    """Write and read json files.

    Parameters
    ----------
    filename : str
        Name of the file. It opens the file like "drawbot/" + filename + ".json".
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
    if data is None:
        data = {}

    filename = f"vars/{filename}.json"

    if mode == "r":
        if not os.path.isfile(filename):
            return data
        try:
            with open(filename) as f:
                return json.load(f)
        except json.decoder.JSONDecodeError as e:
            print(f"An error occurred while reading {filename}: {e}")
            if e.args[0] == "Expecting value: line 1 column 1 (char 0)":
                with open(filename, "w") as f:
                    json.dump(data, f, indent=4)
            return {}

    elif mode == "w":
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
