import os
from dotenv import load_dotenv
from src.files import get_config_env_path, get_directory_path
from argparse import Namespace


class Config:
    def __init__(self, namespace: Namespace) -> None:
        self.starting_directory = get_directory_path(namespace.starting_directory)
        self.parent_page_id = namespace.parent_page_id
        self.file_types = tuple(namespace.file_types)
        self.purge = namespace.purge
        self.cleanup = namespace.cleanup

        load_dotenv(get_config_env_path(namespace.config_env))

        self.url = os.environ.get("CONFLUENCE_BASE_URL")
        self.username = os.environ.get("CONFLUENCE_EMAIL")
        self.password = os.environ.get("ATLASSIAN_TOKEN")
