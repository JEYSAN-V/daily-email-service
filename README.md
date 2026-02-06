# Daily Email Service

Small Python project to send daily emails (entry point: `app.py`).

## Features
- Send scheduled daily emails using your SMTP provider
- Load configuration from environment variables or a `.env` file

## Prerequisites
- Python 3.10+
- Git (optional)

## Setup
1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file (or set environment variables) with SMTP credentials and recipients. Example `.env`:

```env
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=you@example.com
SMTP_PASS=yourpassword
EMAIL_FROM=you@example.com
EMAIL_TO=recipient@example.com
SCHEDULE_TIME=09:00
```

4. Run the app:

```bash
python app.py
```

## Notes
- Update `app.py` to customize email content, scheduling, or add logging.
- Keep credentials out of source control; use environment variables or secrets management.

## License
Add a license if you plan to publish this project.
