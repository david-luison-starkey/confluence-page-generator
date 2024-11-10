from argparse import BooleanOptionalAction, Namespace, ArgumentParser, HelpFormatter
from src.config import Config
from src.files import get_directory_entry_list
from src.macros import CODE_EXTENSION
from atlassian import Confluence
from src.page_generator import (
    cleanup_child_pages,
    create_satac_confluence_pages,
    purge_child_pages,
    set_page_labels,
    validate_target_parent_page,
)


def parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Script to create Confluence pages with language specific code block macros. \
            The Confluence page structure and naming convention follows the folder and file structure \
            found within the starting directory argument.",
        formatter_class=lambda prog: HelpFormatter(prog, max_help_position=80),
    )

    parser.add_argument(
        "-d",
        "--starting-directory",
        required=True,
        help="Starting directory for recursive folder and file search",
    )
    parser.add_argument(
        "-i",
        "--parent-page-id",
        required=True,
        help="Confluence page id of the parent page that new pages will be generated under",
    )
    parser.add_argument(
        "-f",
        "--file-types",
        nargs="+",
        required=True,
        choices=[item["extension"] for item in CODE_EXTENSION],
        help="File extensions to include when searching directories for pages and associated code blocks to create, \
            separated by a space. e.g. -f sql java js json html",
    )
    parser.add_argument(
        "-e",
        "--config-env",
        default="config.env",
        help="Path to .env file with the following properties to drive script: \
            CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, ATLASSIAN_TOKEN",
    )
    parser.add_argument(
        "-p",
        "--purge",
        action=BooleanOptionalAction,
        type=bool,
        default=False,
        help="If present, script will delete all child pages of the --page-id page before performing any other actions, \
            providing a clean slate",
    )
    parser.add_argument(
        "-c",
        "--cleanup",
        action=BooleanOptionalAction,
        type=bool,
        default=False,
        help="If True, cleanup child pages that were not explicitly created or updated as part of script execution",
    )
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    config = Config(args)
    confluence = Confluence(
        url=config.url, username=config.username, password=config.password
    )
    entries = get_directory_entry_list(config.starting_directory, config.file_types)

    if validate_target_parent_page(confluence, config):
        purge_child_pages(confluence, config)
        updated_pages_id_list = create_satac_confluence_pages(
            confluence, config.parent_page_id, entries
        )
        set_page_labels(confluence, updated_pages_id_list)
        cleanup_child_pages(confluence, config, updated_pages_id_list)
    else:
        raise ValueError(
            f"Target Confluence parent page (id: {config.parent_page_id}) is not a valid target"
        )
