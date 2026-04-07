import logging
import random
import asyncio

from telethon import TelegramClient, events
from telethon.sessions import StringSession

from config import API_ID, API_HASH, STRING_SESSION, CHAT_ID, CHANNELS
from filters import classify_message
from db import create_table, is_duplicate, save_job

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)


async def process_message(event):
    """
    Full pipeline with:
    - filtering
    - deduplication
    - randomized delay (anti-spam)
    """
    try:
        text = event.message.text

        if not text:
            return

        category = classify_message(text)
        if not category:
            return

        if is_duplicate(text):
            logger.info("Duplicate skipped")
            return

        # Save job with metadata
        channel_name = event.chat.username or event.chat.title
        save_job(text, category, channel_name)

        logger.info(f"{category.upper()} job from {channel_name}")

        # ⏳ Anti-spam delay (random 2–5 seconds)
        delay = random.uniform(2, 5)
        logger.info(f"Waiting {delay:.2f}s before forwarding...")
        await asyncio.sleep(delay)

        await client.forward_messages(CHAT_ID, event.message)

    except Exception as e:
        logger.error(f"Error: {e}")


def register_handlers():
    for channel in CHANNELS:
        client.add_event_handler(
            process_message,
            events.NewMessage(chats=channel)
        )


def main():
    logger.info("Starting bot...")

    create_table()
    register_handlers()

    client.start()
    logger.info("Bot is running...")

    client.run_until_disconnected()


if __name__ == "__main__":
    main()
