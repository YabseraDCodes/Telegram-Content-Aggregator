import hashlib
import re
import mysql.connector
from difflib import SequenceMatcher

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def create_table():
    """
    Now stores:
    - raw_text
    - category
    - source_channel
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            job_hash VARCHAR(64) UNIQUE,
            raw_text TEXT,
            category VARCHAR(50),
            source_channel VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# ---------- NORMALIZATION ----------
def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    return text.strip()


def generate_hash(text: str) -> str:
    return hashlib.sha256(normalize(text).encode()).hexdigest()


# ---------- SIMILARITY ----------
def is_similar(a: str, b: str, threshold=0.85):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio() >= threshold


def get_recent_jobs(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT raw_text FROM jobs ORDER BY created_at DESC LIMIT %s",
        (limit,)
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in results]


def is_duplicate(text: str):
    conn = get_connection()
    cursor = conn.cursor()

    job_hash = generate_hash(text)

    # Fast check
    cursor.execute("SELECT id FROM jobs WHERE job_hash = %s", (job_hash,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return True

    cursor.close()
    conn.close()

    # Smart check
    for old_text in get_recent_jobs():
        if is_similar(text, old_text):
            return True

    return False


def save_job(text: str, category: str, channel: str):
    """
    Save full job info.
    """
    conn = get_connection()
    cursor = conn.cursor()

    job_hash = generate_hash(text)

    cursor.execute(
        "INSERT INTO jobs (job_hash, raw_text, category, source_channel) VALUES (%s, %s, %s, %s)",
        (job_hash, text, category, channel)
    )

    conn.commit()
    cursor.close()
    conn.close()