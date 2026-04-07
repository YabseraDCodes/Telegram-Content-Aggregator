import os
import json


def get_env_variable(name: str) -> str:
    """
    Fetch environment variables safely.
    """
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


# Telegram config
API_ID = int(get_env_variable("API_ID"))
API_HASH = get_env_variable("API_HASH")
STRING_SESSION = get_env_variable("STRING_SESSION")
CHAT_ID = get_env_variable("CHAT_ID")

# MySQL config (Railway provides these)
DB_HOST = get_env_variable("MYSQLHOST")
DB_USER = get_env_variable("MYSQLUSER")
DB_PASSWORD = get_env_variable("MYSQLPASSWORD")
DB_NAME = get_env_variable("MYSQLDATABASE")


#  LOAD USER FILTERS
def load_filters():
    """
    Load user-defined filters from JSON file.
    """
    with open("filters.json", "r") as f:
        return json.load(f)


FILTERS = load_filters()

CHANNELS = FILTERS["channels"]
IMPORTANT_WORDS = FILTERS["important_words"]
CATEGORIES = FILTERS["categories"]
