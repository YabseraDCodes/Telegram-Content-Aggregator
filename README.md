# Telegram Content Aggregator

A scalable, event-driven Telegram automation system that monitors channels, filters relevant content, removes duplicates, and forwards only useful messages to a target chat.

> This is **not** a Telegram bot.
> It runs using a Telegram user account via the `Telethon` library.

## Why I Built This

As a recent graduate, I was actively searching for job opportunities across multiple Telegram job channels in Ethiopia.

### The Problem

- There are many channels posting vacancies.
- Most posts are irrelevant to my field.
- The same job gets reposted across multiple channels.
- Manually checking each channel is time-consuming and inefficient.

### The Solution

Instead of checking channels every day manually, I built this system to:

- Automatically monitor job channels.
- Filter only jobs I am interested in.
- Remove duplicate postings.
- Send relevant opportunities directly to my personal Telegram channel.

## Current Use Case

### Job Filtering Automation

- Tracks selected Telegram channels.
- Filters jobs based on user-defined interests.
- Sends only relevant jobs to a private channel.

## How It Works

1. Listens to new messages from selected Telegram channels.
2. Filters messages using keywords and categories.
3. Removes duplicates using:
   - Hashing (fast)
   - Similarity matching (smart)
4. Stores results in a database.
5. Waits randomly (2-5 seconds) to avoid spam detection.
6. Forwards filtered messages to your Telegram chat.

## `filters.json` (User-Defined Configuration)

This is the core customization file. You do **not** need to change the code; just edit this file.

```json
{
  "channels": [
    "freelance_ethio",
    "ethiojobsofficial"
  ],
  "important_words": ["apply", "deadline", "requirements"],
  "categories": {
    "software": ["python", "backend", "developer"],
    "data": ["data analyst", "ai", "machine learning"]
  }
}
```

### `channels`

- List of Telegram channel usernames (no links needed).
- Example values:
  - `freelance_ethio`
  - `ethiojobsofficial`

### `important_words`

- Acts as a second-level filter.
- A message must contain at least one of these words to pass.
- Helps eliminate noise.

### `categories`

- Defines job categories and their keywords.
- Used to classify messages.

Example:

```json
"software": ["python", "backend"]
```

If a message contains any of these keywords, it is classified as `software`.

## Database (MySQL)

### Stored Fields

- Full message text
- Category
- Source channel
- Timestamp

### Used For

- Duplicate detection
- Future analytics
- Data reuse

## Project Structure

```text
Telegram-Content-Aggregator/
|-- main.py
|-- config.py
|-- filters.py
|-- db.py
|-- filters.json
```

### `main.py`

Entry point of the application. Handles:

- Receiving messages
- Processing pipeline
- Forwarding messages

### `config.py`

- Loads environment variables
- Loads `filters.json`
- Central place for configuration

### `filters.py`

- Contains filtering logic
- Classifies messages into categories
- Applies keyword rules

### `db.py`

- Handles database operations
- Stores jobs
- Implements duplicate detection via:
  - Hashing
  - Similarity matching

### `filters.json`

- User-controlled filtering rules
- Makes the system flexible without code changes

## Telegram Setup

### 1. Get `API_ID` and `API_HASH`

1. Go to: <https://my.telegram.org>
2. Log in with your Telegram account.
3. Click **API development tools**.
4. Create an app.

You will receive:

- `API_ID`
- `API_HASH`

### 2. Generate `STRING_SESSION`

Install Telethon and run:

```python
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print(client.session.save())
```

Then:

- Log in once.
- Copy the printed string.
- Use it as `STRING_SESSION`.

### 3. Set `CHAT_ID`

This is where messages will be sent. You can use your private channel username.

Example:

```text
my_jobs_channel
```

## Environment Variables

```env
API_ID=
API_HASH=
STRING_SESSION=
CHAT_ID=
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
```

## Deployment (Railway)

This project is deployed on Railway as a worker service.

- Runs continuously
- Listens to Telegram channels
- Automatically processes and forwards messages

`Procfile`:

```procfile
worker: python main.py
```

## Rate Limiting (Important)

The system includes a random delay (2-5 seconds) before forwarding messages.

Keep this enabled to reduce risk of:

- `429 Too Many Requests` errors
- Temporary Telegram limits
- Permanent account restrictions

## Scalability

This system is not limited to job filtering. It can be adapted for:

- News aggregation
- Crypto signals
- Scholarship alerts
- Market monitoring
- Any keyword-based content tracking

## Database Flexibility

Currently uses MySQL, but can be adapted to:

- PostgreSQL
- SQLite
- MongoDB

Only `db.py` needs modification.

## Screenshots

Add your own:

- Railway deployment logs
  
  <img width="1843" height="852" alt="Screenshot AAA" src="https://github.com/user-attachments/assets/6ada214e-5014-4765-b2bc-1ab1a82aaf1a" />

  
- Database table
  
  <img width="1853" height="854" alt="Screenshot AAA 2026-04-07 165730" src="https://github.com/user-attachments/assets/cd873f59-b8d6-4905-ac8d-55fa68d48829" />


- How enviroment variables are kept
  
  <img width="1853" height="855" alt="Screenshot 2026-04-07 184851" src="https://github.com/user-attachments/assets/671af747-375d-4925-a06d-3595c3463039" />



- Forwarded jobs  based on my prefrence
  
  <img width="1123" height="1005" alt="Screenshot 2026-04-07 163709" src="https://github.com/user-attachments/assets/a712bc50-a3d6-4f41-838a-314712df652a" />

