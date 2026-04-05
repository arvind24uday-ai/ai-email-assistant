import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="AI Email Assistant", layout="wide")

st.title("📧 AI Email Assistant Dashboard")
st.write("Analyze emails and identify important ones")

# Upload CSV
uploaded_file = st.file_uploader("Upload Email CSV", type=["csv"])

# Classifier
def classify_email(subject):
    subject = str(subject).lower()

    important_keywords = [
        "job", "interview", "application",
        "security", "alert", "meeting",
        "urgent", "action", "request"
    ]

    for word in important_keywords:
        if word in subject:
            return "IMPORTANT"

    return "NOT IMPORTANT"

# Reply generator
def generate_reply(subject):
    return f"""Dear Sir/Madam,

Thank you for your email regarding "{subject}". I will review it and respond shortly.

Best regards,
Arvind Uday M"""

# Process file
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Subject" not in df.columns:
        st.error("CSV must contain a 'Subject' column")
    else:
        df["Category"] = df["Subject"].apply(classify_email)

        st.subheader("📊 All Emails")
        st.dataframe(df)

        important_df = df[df["Category"] == "IMPORTANT"]

        st.subheader("✅ Important Emails")
        st.dataframe(important_df)

        if not important_df.empty:
            important_df["Reply"] = important_df["Subject"].apply(generate_reply)

            st.subheader("🤖 Suggested Replies")
            st.dataframe(important_df[["Subject", "Reply"]])

else:
    st.info("Upload a CSV file to get started")
