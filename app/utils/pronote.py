import time
from typing import DefaultDict, Generator, Optional
from collections import defaultdict

from app.utils import json_wr

import pronotepy


def fetch_homeworks(pronote_client: pronotepy.Client) -> Optional[Generator]:
    fetched_homeworks = pronote_client.homework(pronote_client.start_day)

    homeworks: DefaultDict[str, list] = defaultdict(list)
    for homework in fetched_homeworks:
        homeworks[str(homework.date)].append(
            {
                "subject": homework.subject.name,
                "description": homework.description.replace("\n", " ")
            }
        )

    homeworks_file = json_wr("devoirs")
    if homeworks == homeworks_file:
        return

    json_wr("devoirs", "w", homeworks)

    homeworks_list: list = []
    for key, value in homeworks.items():
        for i in value:
            i["date"] = key
        homeworks_list.extend(value)

    homeworks_old_list: list = []
    for key, value in homeworks_file.items():
        for i in value:
            i["date"] = key
        homeworks_old_list.extend(value)

    for homework in homeworks_list:
        if homework in homeworks_old_list:
            continue

        yield homework
