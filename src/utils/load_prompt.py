from typing import Optional
from pathlib import Path
from src.configs.logger import setup_logger

logger = setup_logger(__name__)


class PromptTemplate:
    """
    Utility class to load the prompt template from the text files.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_prompt_template(filename: str) -> Optional[str]:
        """
        Reads the text content from the text file.

        Args:
            filename (str): Path to the file.

        Returns:
            Optional[str]: Content of the file as a string if successful, otherwise None.
        """

        file_path = Path.cwd() / (filename)

        if not file_path.exists():
            logger.error(f"File not found: `{filename}`")
            return None

        try:
            with file_path.open("r", encoding="utf-8") as file:
                content = file.read()
            logger.info(f"File loaded successfully: `{file_path}`")
            return content
        except PermissionError:
            logger.error(f"Permission denied when accessing: `{file_path}`")
        except OSError as e:
            logger.error(f"OS error while reading `{file_path}`: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Unexpected error reading `{file_path}`: {e}", exc_info=True)

        return None