import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import requests
import pymongo
from datetime import datetime, date, timezone

load_dotenv()

# -------------------- EMAIL HELPERS --------------------

def format_content(json_data):
    html_content = f"<h3>{json_data['title']}</h3>"
    html_content += f"<p>Difficulty : {json_data['difficulty']}</p>"
    html_content += json_data["html_description"]
    html_content += (
        f"<p>Problem Link: "
        f"<a href='{json_data['problem_url']}'>{json_data['problem_url']}</a></p>"
    )

    if json_data.get("article_url"):
        html_content += (
            f"<p>Article Link: "
            f"<a href='{json_data['article_url']}'>{json_data['article_url']}</a></p>"
        )
    return html_content


def send_html_email(sender_email, sender_password, receiver_email, subject, html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"✅ Sent → {receiver_email} | {subject}")
    except Exception as e:
        print(f"❌ Email error ({receiver_email}): {e}")
    finally:
        server.quit()


# -------------------- UTILS --------------------

def sent_today(last_sent_date):
    if not last_sent_date:
        return False
    return last_sent_date.date() == datetime.now(timezone.utc).date()



# -------------------- ENV & DB --------------------

SENDER = os.getenv("SENDER")
PASSWORD = os.getenv("PASSWORD")
MONGO_URI = os.getenv("MONGO_URI")
GFG_API = os.getenv("GFG_API")
LC_API = os.getenv("LC_API")

client = pymongo.MongoClient(MONGO_URI)
collection = client["just-one-user-db"]["users"]

# -------------------- FETCH CONTENT ONCE --------------------

gfg_content = requests.get(GFG_API, timeout=180).json()
lc_content  = requests.get(LC_API, timeout=180).json()

gfg_html = format_content(gfg_content)
lc_html = format_content(lc_content)

# -------------------- MAIN JOB --------------------

def run_email_job():
    users = collection.find()

    for user in users:
        email = user.get("email")
        platforms = user.get("preferences", {}).get("platforms", [])
        last_sent = user.get("lastSent", {})

        # ---- GFG ----
        if "gfg" in platforms and not sent_today(last_sent.get("gfg")):
            send_html_email(
                SENDER,
                PASSWORD,
                email,
                "Your Daily Coding Problem - GeeksforGeeks",
                gfg_html,
            )
            collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"lastSent.gfg": datetime.now(timezone.utc)}}
            )

        # ---- LEETCODE ----
        if "leetcode" in platforms and not sent_today(last_sent.get("leetcode")):
            send_html_email(
                SENDER,
                PASSWORD,
                email,
                "Your Daily Coding Problem - LeetCode",
                lc_html,
            )
            collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"lastSent.leetcode": datetime.now(timezone.utc)}}
            )




if __name__ == "__main__":
    run_email_job()
