import logging
import unicodedata

logger = logging.getLogger(__name__)


class WordsUtil:
    """Utility class for handling file paths."""
    
    @staticmethod
    def remove_accents(text: str) -> str:
        normalized_text = unicodedata.normalize("NFD", text)
        text_no_accents = "".join(
            c for c in normalized_text if unicodedata.category(c) != "Mn"
        )
        return text_no_accents