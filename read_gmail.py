import os
import base64
import re
import mimetypes
import pickle
import time
import requests
import schedule

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# --- Google Gmail API Scope ---
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# --- Telegram Config ---
TELEGRAM_BOT_TOKEN = "7984201585:AAGnBwD42rv4wd8hPAtwsfDzaFR0hBiBGJY"  # Replace with your bot token
TELEGRAM_CHAT_ID = "1240116510"                                       # Replace with your chat ID

# --- Gmail Auth Setup ---
def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# --- ML Model & Vectorizer ---
model = pickle.load(open('phishing_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

def predict_email(text):
    cleaned = re.sub(r'\s+', ' ', text.strip())
    vect = vectorizer.transform([cleaned])
    pred = model.predict(vect)[0]
    return pred

# --- Extract Email Parts ---
def extract_email_body(payload):
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                return base64.urlsafe_b64decode(part['body']['data']).decode()
    return ""

def get_attachments(payload):
    attachments = []
    if 'parts' in payload:
        for part in payload['parts']:
            filename = part.get("filename")
            body = part.get("body", {})
            if filename and 'attachmentId' in body:
                mime = part.get("mimeType", "unknown")
                attachments.append((filename, mime))
    return attachments

def extract_links(text):
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.findall(text)

def is_suspicious_link(url):
    return bool(re.search(r'(bit\.ly|tinyurl|\.ru|\.tk|://\d+\.\d+\.\d+\.\d+)', url))

# ✅ Telegram Notification
def send_telegram_alert(subject, sender, links):
    message = f"🚨 *PHISHING DETECTED!*\n\n*Subject:* {subject}\n*From:* {sender}"
    if links:
        message += "\n*Links:*\n" + "\n".join(links)

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        res = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=payload)
        if res.status_code != 200:
            print("❌ Telegram alert failed.")
    except Exception as e:
        print(f"⚠️ Telegram error: {e}")

# 🔁 Email Fetcher
def fetch_emails(query="", label="INBOX", max_results=10, unread_only=True):
    service = get_gmail_service()
    search_query = f"is:unread {query}" if unread_only else query

    results = service.users().messages().list(userId='me', labelIds=[label], q=search_query, maxResults=max_results).execute()
    messages = results.get('messages', [])
    all_emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get('payload', {})
        headers = payload.get('headers', [])
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
        sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")

        body = extract_email_body(payload)
        prediction = predict_email(body)
        attachments = get_attachments(payload)
        links = extract_links(body)

        all_emails.append({
            'subject': subject,
            'sender': sender,
            'body': body,
            'prediction': prediction,
            'attachments': attachments,
            'links': links,
        })

    return all_emails

# ✅ Main Auto Scan Loop (No feedback)
def auto_check_and_alert():
    emails = fetch_emails(max_results=10, unread_only=True)
    if not emails:
        print("📭 No unread emails found.")
    else:
        print(f"\n📬 Scanning {len(emails)} unread emails...\n")
        for i, email in enumerate(emails):
            print(f"\n📩 Email #{i+1}: {'🚨 PHISHING' if email['prediction'] == 0 else '✅ SAFE'}")
            print("-" * 40)
            print(f"📝 Subject: {email['subject']}")
            print(f"👤 From: {email['sender']}")
            print(f"📄 Body:\n{email['body'][:500]}...\n")

            if email['attachments']:
                print("📎 Attachments:")
                for fname, mime in email['attachments']:
                    print(f" - {fname} ({mime})")
                    if fname.lower().endswith(('.exe', '.bat', '.scr', '.vbs')):
                        print("   ⚠️ Suspicious file type!")
            else:
                print("📎 No attachments.")

            if email['links']:
                print("\n🔗 Links Found:")
                for link in email['links']:
                    print(f" - {link} {'⚠️' if is_suspicious_link(link) else ''}")
            else:
                print("🔗 No links found.")
            print("=" * 60)

            # ✅ Send Telegram alert if phishing
            if email['prediction'] == 0:
                send_telegram_alert(email['subject'], email['sender'], email['links'])

# 🔄 Scheduler Loop
if __name__ == "__main__":
    schedule.every(5).minutes.do(auto_check_and_alert)
    print("🚀 Phishing Email Scanner running every 5 minutes...\n")

    while True:
        schedule.run_pending()
        time.sleep(1)
