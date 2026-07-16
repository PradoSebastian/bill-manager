import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class PathUtil:
    """Utility class for handling file paths."""
    
    @staticmethod
    def get_full_path(path: str) -> str:
        """Returns the full path to a file or directory."""
        BASE_DIR = Path(__file__).resolve().parent
        return str(BASE_DIR.parent / path).replace('\\', '/')

    @staticmethod
    def read_json_files_from_folder(
        folder_path: str
    ) -> list[dict[str, Any]]:
        """Reads JSON files from the specified folder and returns a list of dictionaries."""
        json_files: list[dict[str, Any]] = []
        for file_path in Path(folder_path).glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                json_files.append(data)
        return json_files