import json
from os import path
from typing import Optional, Dict, Union, List, Any

JsonDict = Dict[str, Any]
JsonList = List[Any]
JsonData = Union[JsonDict, JsonList]


def json_wr(
    file_path: str,
    data: Optional[JsonData] = None
) -> Optional[JsonData]:
    """Read json data or write given data with given file path."""
    if not path.exists(file_path):
        return

    with open(
        f"app/{file_path}.json",
        'r' if data is None else 'w+'
    ) as json_file:

        if data is None:
            return json.load(json_file)

        json.dump(data, json_file, indent=4)
