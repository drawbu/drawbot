from typing import DefaultDict, Generator, Optional
from collections import defaultdict

from .json_files import JsonData
from utils import json_wr
import pronotepy


def fetch_homeworks(pronote_client: pronotepy.Client) -> Optional[Generator]:
    fetched_homeworks = pronote_client.homework(pronote_client.start_day)

    homeworks: DefaultDict[str, list] = defaultdict(list)
    for homework in fetched_homeworks:
        homeworks[str(homework.date)].append(
            {
                "subject": homework.subject.name,
                "description": homework.description.replace("\n", " "),
            }
        )

    yield from fetch_from_json("devoirs", homeworks)


def fetch_grades(pronote_client: pronotepy.Client) -> Optional[Generator]:
    fetched_grades = pronote_client.periods[0].grades

    grades: DefaultDict[str, list] = defaultdict(list)
    for g in fetched_grades:
        grades[str(g.date)].append(
            {
                "subject": g.subject.name,
                "comment": g.comment,
                "grade": f"{g.grade}/{g.out_of}",
                "average": f"{g.average}/{g.out_of}",
                "coefficient": f"{g.coefficient}",
                "max": f"{g.max}/{g.out_of}",
                "min": f"{g.min}/{g.out_of}",
            }
        )

    yield from fetch_from_json("grades", grades)


def fetch_from_json(filename: str, json_data: JsonData) -> Generator:
    json_file = json_wr(filename)

    if json_data == json_file:
        return

    json_wr(filename, "w", json_data)

    if json_file == {}:
        print("Première exécution, le générateur ne va rien renvoyer.")
        return

    json_vals: list = []
    for key, value in json_data.items():
        for i in value:
            i["date"] = key
        json_vals.extend(value)

    old_vals: list = []
    for key, value in json_file.items():
        for i in value:
            i["date"] = key
        old_vals.extend(value)

    for value in json_vals:
        if value in old_vals:
            continue

        yield value
