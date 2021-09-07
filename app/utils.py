import json
from os import path
from typing import Optional, List, Dict, Union

from app import JsonData


def json_wr(
        file_path: str,
        data: Optional[JsonData] = None,
        if_none: Optional[Union[Dict, List]] = None
) -> Optional[JsonData]:
    """
    Read json data or write given data with given file path.

    file_path: path of the file to write inside
    data: data to write inside the file (optional)
    if_none: if you're trying to read the file and it does not exist
             it will return this
    """
    with open(
            f"app/{file_path}.json",
            'r' if data is None
            and if_none is None
            else 'w+'
    ) as json_file:

        if data is None and if_none is None:
            return json.load(json_file)

        if data is not None:
            json.dump(data, json_file, indent=4)
            return

        return if_none
