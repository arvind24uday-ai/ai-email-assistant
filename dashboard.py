import streamlit as st
import pandas as pd

# ===============================
# 🔥 UI STYLE (OPTION 3)
# ===============================
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🔥 TITLE
# ===============================
st.title("📧 AI Email Assistant Dashboard")
st.write("Analyze emails and identify important ones")

# ===============================
# 🔥 OPTION 1: SAMPLE DATA BUTTON
# ===============================
sample_data_clicked = st.button("📊 Load Sample Data")

# Upload CSV
uploaded_file = st.file_uploader("Upload Email CSV", type=["csv"])


# ===============================
# 🔹 CLASSIFIER FUNCTION
# ===============================
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


# ===============================
# 🔹 REPLY GENERATOR
# ===============================
def generate_reply(subject):
    return f"""Dear Sir/Madam,

Thank you for your email regarding "{subject}". I will review it and respond shortly.

Best regards,
Arvind Uday M"""


# ===============================
# 🔥 DATA HANDLING (UPLOAD OR SAMPLE)
# ===============================
df = None

# Sample data
if sample_data_clicked:
    data = {
        "Subject": [
            "Interview scheduled with Google",
            "50% discount on shoes",
            "Security alert on your account",
            "Weekly newsletter",
            "Job application update"
        ]
    }
    df = pd.DataFrame(data)

# Uploaded file
elif uploaded_file:
    df = pd.read_csv(uploaded_file)


# ===============================
# 🔥 PROCESS DATA
# ===============================
if df is not None:

    if "Subject" not in df.columns:
        st.error("CSV must contain a 'Subject' column")

    else:
        # Classification
        df["Category"] = df["Subject"].apply(classify_email)

        # ===============================
        # 🔥 OPTION 2: CHART
        # ===============================
        st.subheader("📈 Email Distribution")
        chart_data = df["Category"].value_counts()
        st.bar_chart(chart_data)

        # Show all emails
        st.subheader("📊 All Emails")
        st.dataframe(df)

        # Filter important emails
        important_df = df[df["Category"] == "IMPORTANT"]

        st.subheader("✅ Important Emails")
        st.dataframe(important_df)

        # Generate replies
        if not important_df.empty:
            important_df["Reply"] = important_df["Subject"].apply(generate_reply)

            st.subheader("🤖 Suggested Replies")
            st.dataframe(important_df[["Subject", "Reply"]])

else:
    st.info("Upload a CSV file or click 'Load Sample Data' to get started")
    
