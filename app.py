# app.py
import streamlit as st
import pickle
import re
from read_gmail import fetch_emails

# Load ML model & vectorizer
model = pickle.load(open("phishing_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Utility function
def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip())

def is_suspicious_file(filename):
    return filename.lower().endswith(('.exe', '.bat', '.scr', '.vbs'))

def is_suspicious_link(url):
    return bool(re.search(r'(bit\.ly|tinyurl|\.ru|\.tk|://\d+\.\d+\.\d+\.\d+)', url))

# --- Streamlit UI ---
st.set_page_config(page_title="Phishing Email Detector", layout="wide")
st.title("📧 Gmail Phishing Email Detector")

st.sidebar.header("🔍 Choose Detection Mode")
mode = st.sidebar.radio("Select input mode:", ["📥 Gmail Inbox Scan", "✍️ Manual Email Input"])

# Gmail Inbox Scan Mode
if mode == "📥 Gmail Inbox Scan":
    st.subheader("📥 Scan Gmail Inbox for Suspicious Emails")

    search_query = st.text_input("🔎 Search emails with keyword (optional)", placeholder="e.g., invoice, login reset")
    filter_option = st.radio("📬 Fetch from:", ["Unread Emails", "All Emails"])

    if st.button("Fetch Emails"):
        unread_only = filter_option == "Unread Emails"
        with st.spinner("🔄 Fetching and scanning emails..."):
            emails = fetch_emails(query=search_query, max_results=10, unread_only=unread_only)

        if not emails:
            st.info("📭 No matching emails found.")
        else:
            for idx, email in enumerate(emails):
                with st.expander(f"📨 Email #{idx+1} - {email['subject']}"):
                    st.write(f"**From:** {email['sender']}")
                    st.write(f"**Subject:** {email['subject']}")
                    st.markdown("**📄 Body Preview:**")
                    st.code(email['body'][:500] + "..." if len(email['body']) > 500 else email['body'])

                    prediction = model.predict(vectorizer.transform([email['body']]))[0]
                    result_label = "PHISHING" if prediction == 0 else "SAFE"
                    st.markdown(f"### 🧠 Prediction: {'🚨' if prediction == 0 else '✅'} This email is **{result_label}**")

                    st.markdown("**📎 Attachments (if any):**")
                    if email.get("attachments"):
                        for fname, mime in email["attachments"]:
                            if is_suspicious_file(fname):
                                st.warning(f"⚠️ {fname} - Suspicious file type!")
                            else:
                                st.write(f"• {fname}")
                    else:
                        st.write("No attachments.")

                    st.markdown("**🔗 Links Found:**")
                    if email.get("links"):
                        for link in email["links"]:
                            if is_suspicious_link(link):
                                st.warning(f"⚠️ {link} - Suspicious!")
                            else:
                                st.write(f"• {link}")
                    else:
                        st.write("No links found.")

# Manual Input Mode
elif mode == "✍️ Manual Email Input":
    st.subheader("✍️ Manually Paste Email Content")
    user_input = st.text_area("📄 Paste the email content here:")

    if st.button("🔍 Check Email"):
        if user_input.strip() == "":
            st.warning("⚠️ Please enter some email content.")
        else:
            cleaned = clean_text(user_input)
            input_vector = vectorizer.transform([cleaned])
            prediction = model.predict(input_vector)[0]

            if prediction == 0:
                st.error("🚨 This email is **PHISHING**!")
            else:
                st.success("✅ This email is **SAFE**.")
