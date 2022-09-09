"""Utilities for drawbot."""
from .json_files import json_wr, JsonData, JsonDict, JsonList
from .pronote import fetch_homeworks, fetch_grades, chunks

__all__ = (
    "json_wr",
    "fetch_homeworks",
    "fetch_grades",
    "JsonData",
    "JsonDict",
    "JsonList",
    "chunks"
)
