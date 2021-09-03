import json
from os import path
from typing import Optional

from app import JsonData


def json_wr(
    file_path: str,
    data: Optional[JsonData] = None
) -> Optional[JsonData]:
    """Read json data or write given data with given file path."""
    if not path.exists(f'app/{file_path}.json'):
        return

    with open(
        f"app/{file_path}.json",
        'r' if data is None else 'w+'
    ) as json_file:

        if data is None:
            return json.load(json_file)

        json.dump(data, json_file, indent=4)
