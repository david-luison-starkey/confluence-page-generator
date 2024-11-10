from typing import List
from pathlib import Path
from src.config import Config
from src.files import DirectoryEntry, get_file_contents, get_file_extension
from src.macros import (
    get_code_block_macro_string,
    get_page_tree_macro_string,
    get_table_contents_macro_string,
    CODE_EXTENSION,
)
from atlassian import Confluence


def get_code_block_heading(path: str) -> str:
    return get_formatted_heading(Path(path).stem)


def get_formatted_heading(heading: str) -> str:
    return f"<h2> {heading} </h2>"


def get_code_macro_code_type(path: str) -> str:
    return "".join(
        [
            item["code"]
            for item in CODE_EXTENSION
            if item["extension"] == get_file_extension(path)
        ]
    )


def is_directory_entry_children_also_have_populated_children(
    child_entries: List[DirectoryEntry],
) -> bool:
    for entry in child_entries:
        if entry["files"]:
            # If a child folder has files we want to create a parent page with the page tree macro
            return True
        elif entry["children"]:
            # If a child folder has no files but has children of its own, keep checking recursively
            return is_directory_entry_children_also_have_populated_children(
                entry["children"]
            )
        else:
            # dont return False here as we want to exhaust all possible recursive calls
            continue
    # If no child folders have any files in them, don't create parent page or child pages,
    # since no content exists in tree
    return False


def get_page_code_block_content(file_list: List[str]) -> str:
    confluence_page_content = ""

    if len(file_list) > 2:
        # Only create table of contents if there's 3 or more code blocks
        confluence_page_content = get_table_contents_macro_string()
        confluence_page_content += "\n"

    for file in file_list:
        code_macro_code = get_code_macro_code_type(file)
        code_block = get_file_contents(file)
        code_block_heading = get_code_block_heading(file)
        confluence_page_content += code_block_heading
        confluence_page_content += "\n"
        confluence_page_content += get_code_block_macro_string(
            code_block, language=code_macro_code
        )
        confluence_page_content += "\n"
    return confluence_page_content


def create_satac_confluence_pages(
    confluence: Confluence, parent_page_id: str, entries: List[DirectoryEntry]
) -> List[str]:
    updated_created_page_ids = []

    for item in entries:
        title = item["folder"]

        if (
            not item["files"]
            and item["children"]
            and is_directory_entry_children_also_have_populated_children(
                item["children"]
            )
        ):
            confluence_page_content = get_page_tree_macro_string()
            response = confluence.update_or_create(
                parent_page_id,
                title,
                confluence_page_content,
                representation="storage",
                full_width=False,
            )
            page_id = response["id"]
            updated_created_page_ids.append(page_id)
            updated_created_page_ids.extend(
                create_satac_confluence_pages(confluence, page_id, item["children"])
            )

        elif item["files"]:
            confluence_page_content = get_page_code_block_content(item["files"])
            response = confluence.update_or_create(
                parent_page_id,
                title,
                confluence_page_content,
                representation="storage",
                full_width=False,
            )
            page_id = response["id"]
            updated_created_page_ids.append(page_id)

            if item["children"]:
                updated_created_page_ids.extend(
                    create_satac_confluence_pages(confluence, page_id, item["children"])
                )

    return updated_created_page_ids


def purge_child_pages(confluence: Confluence, config: Config) -> None:
    if config.purge:
        child_pages = confluence.get_child_id_list(config.parent_page_id)
        for page_id in child_pages:
            confluence.remove_page(page_id, recursive=True)


def cleanup_child_pages(
    confluence: Confluence, config: Config, retain_pages: List[str]
) -> None:
    if config.cleanup:
        delete_pages = set(confluence.get_child_id_list(config.parent_page_id)) - set(
            retain_pages
        )
        for page_id in delete_pages:
            print(f"Deleting page with id: {page_id} (and child pages)")
            confluence.remove_page(page_id, recursive=True)


def set_page_labels(
    confluence: Confluence, page_id_list: List[str], label: str = "generated"
) -> None:
    for page_id in page_id_list:
        confluence.set_page_label(page_id, label)


def validate_target_parent_page(confluence: Confluence, config: Config) -> bool:
    response = confluence.get_page_by_id(config.parent_page_id)
    return (
        response["title"] == "SQLs anchor page"
        and response["space"]["key"] == "~satds"
        and response["space"]["type"] == "personal"
    )
