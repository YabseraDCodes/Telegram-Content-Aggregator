import re
from config import CATEGORIES, IMPORTANT_WORDS

CATEGORY_PATTERNS = {
    category: re.compile(r"\b(" + "|".join(keywords) + r")\b")
    for category, keywords in CATEGORIES.items()
}


def classify_message(text: str):
    """
    Determine if message matches a job category.
    """
    text_lower = text.lower()

    for category, pattern in CATEGORY_PATTERNS.items():
        if pattern.search(text_lower):
            if any(word in text_lower for word in IMPORTANT_WORDS):
                return category

    return None