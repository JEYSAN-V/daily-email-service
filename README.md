## Daily Email Service

Sends a daily “Problem of the Day” email to users based on their preferences, using:
- Gmail SMTP (HTML email)
- MongoDB (to store users + last sent timestamps)
- 2 external “POTD” APIs (GeeksforGeeks + LeetCode)

The entire job currently lives in `app.py` and is meant to be run on a schedule (daily).

---

## What it does (high level)

When you run `python app.py`:

1. Loads environment variables from `.env`
2. Connects to MongoDB
3. Fetches today’s problems from Custom API :
   - `GFG_API`
   - `LC_API`
4. Loops through every user document and, per platform:
   - Sends the HTML email if the user is opted in **and** they have not been sent an email “today” (UTC)
   - Updates `lastSent.<platform>` in MongoDB

Platforms supported by the code:
- `gfg`
- `leetcode`

---

## Project structure

- `app.py`: main scheduled job (fetch content → email users → update DB)
- `requirements.txt`: Python dependencies
- `.env`: local secrets (ignored by git)

---

## Prerequisites

- Python 3.10+ recommended
- A MongoDB instance (Atlas or self-hosted)
- A Gmail account + **Gmail App Password** (recommended) for SMTP

---

## Setup (local)

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create your env file:
```bash
SENDER=
PASSWORD=
MONGO_URI=
GFG_API=
LC_API=
```

Run once:

```bash
python app.py
```

---

## Environment variables

These are required by `app.py`:

- **`MONGO_URI`**: MongoDB connection string
- **`GFG_API`**: URL that returns a JSON payload for the GFG POTD
- **`LC_API`**: URL that returns a JSON payload for the LeetCode POTD
- **`SENDER`**: Gmail address used to send emails
- **`PASSWORD`**: Gmail App Password (or SMTP password) for `SENDER`

---

## MongoDB data model (required shape)

### Database
- **Name:** `<your_database_name>`

### Collection
- **Name:** `<your_collection_name>`

Each user document should look like:

```json
{
  "email": "person@example.com",
  "preferences": {
    "platforms": ["gfg", "leetcode"]
  },
  "lastSent": {
    "gfg": "2026-02-06T05:12:34.000Z",
    "leetcode": "2026-02-06T05:12:34.000Z"
  }
}
```

Field behavior:
- `preferences.platforms` controls which emails a user receives.
- `lastSent.gfg` and `lastSent.leetcode` are set by the script after successful sends.
- “Sent today” is checked in **UTC**.

---

## POTD API response shape

Both `GFG_API` and `LC_API` are expected to return JSON containing at least:

- `title`
- `difficulty`
- `html_description`
- `problem_url`

Optional:
- `article_url`

This is used to generate the HTML email body.

---

## Scheduling (run daily)

This repo is designed to be run by a scheduler:

### Windows Task Scheduler (example)

- Program/script: `python`
- Add arguments: `app.py`
- Start in: the project folder (where `app.py` is)

Make sure the task runs with:
- The correct Python (venv if you use one)
- Access to your `.env` file (the working directory matters)

---

## Troubleshooting

- **SMTP authentication fails**
  - Use a Gmail **App Password** (recommended) and ensure 2FA is enabled on the Google account.
  - Confirm `SENDER` and `PASSWORD` match the same account.

- **MongoDB connection fails**
  - Confirm IP allowlist (Atlas), username/password, and database/cluster name in `MONGO_URI`.

- **POTD API errors / timeouts**
  - The script uses `timeout=180`. If an API is down, the run will fail before any emails send (because it fetches content once at startup).

---
