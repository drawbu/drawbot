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
                "min": f"{g.min}/{g.out_of}"
            }
        )

    grades_file = json_wr("grades")
    if grades == grades_file:
        return

    json_wr("grades", "w", grades)

    grades_list: list = []
    for key, value in grades.items():
        for i in value:
            i["date"] = key
        grades_list.extend(value)

    grades_old_list: list = []
    for key, value in grades_file.items():
        for i in value:
            i["date"] = key
        grades_old_list.extend(value)

    for grade in grades_list:
        if grade in grades_old_list:
            continue

        yield grade
