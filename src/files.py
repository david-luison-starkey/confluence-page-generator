from __future__ import annotations
from typing import TypedDict, List, Tuple
import os


class DirectoryEntry(TypedDict):
    folder: str
    files: List[str]
    children: List[DirectoryEntry]


def get_config_env_path(env_file: str) -> str:
    path = os.path.abspath(env_file)
    if os.path.exists(path) and os.path.isfile(path) and env_file.endswith(".env"):
        return path

    else:
        raise FileNotFoundError(
            "Provide the name of the .env config file (if in script directory), or its absolute path"
        )


def get_directory_path(directory: str) -> str:
    path = os.path.abspath(directory)
    if os.path.exists(path) and os.path.isdir(path):
        return path
    else:
        raise OSError("Provide a valid starting directory path (relative or absolute)")


def get_file_contents(path: str) -> str:
    page_body = ""
    with open(path, "r") as file:
        for line in file:
            page_body += line
    return page_body.rstrip("\n")


def get_file_extension(path: str) -> str:
    return os.path.splitext(path)[1][1:]


def build_directory_entry(path: str, file_types: Tuple[str, ...]) -> DirectoryEntry:
    files = []
    children = []
    for item in os.listdir(path):
        item_path = os.path.join(os.path.abspath(path), item)
        if os.path.isfile(item_path) and item_path.endswith(file_types):
            files.append(item_path)
        elif os.path.isdir(item_path):
            children.append(build_directory_entry(item_path, file_types))

    entry: DirectoryEntry = {
        "folder": get_page_title_from_folder_name(os.path.basename(path)),
        "files": files,
        "children": children,
    }
    return entry


def get_directory_entry_list(
    starting_directory: str, file_types: Tuple[str, ...]
) -> List[DirectoryEntry]:
    path = get_directory_path(starting_directory)
    return [build_directory_entry(path, file_types)]


def get_page_title_from_folder_name(folder: str) -> str:
    return folder.replace("_", " ").lstrip(" ").title()
