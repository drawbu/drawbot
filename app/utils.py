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
    open_mode = 'r' if data is None else 'w+'
    exists = True
    if not path.exists(f'app/{file_path}.json'):
        exists = False
        open_mode = 'w+'

    with open(
            f"app/{file_path}.json",
            open_mode
    ) as json_file:

        if exists:
            if data is None:
                return json.load(json_file)

            json.dump(data, json_file, indent=4)
            return

        if if_none is None:
            json.dump(data, json_file, indent=4)
            return
        return if_none
