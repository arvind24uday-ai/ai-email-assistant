import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AI Email Assistant", layout="wide")

st.title("📧 AI Email Assistant Dashboard")
st.write("Analyze emails and identify important ones")

# 🔹 Load Sample Data
if st.button("📊 Load Sample Data"):
    st.session_state["use_sample"] = True

uploaded_file = st.file_uploader("Upload Email CSV", type=["csv"])

# 🔹 Load Data
if "use_sample" in st.session_state and st.session_state["use_sample"]:
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

elif uploaded_file:
    df = pd.read_csv(uploaded_file)

else:
    st.info("Upload a CSV file or click 'Load Sample Data'")
    st.stop()

# 🔹 AI Classification
def classify_email(subject):
    keywords = ["interview", "job", "security", "alert", "application"]
    return "IMPORTANT" if any(word in subject.lower() for word in keywords) else "NOT IMPORTANT"

df["Category"] = df["Subject"].apply(classify_email)

# 🔹 REAL AI Reply (Ollama local)
def generate_ai_reply(subject):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"""
Write a short professional reply (3 lines max).

Email subject: {subject}

Start with Dear,
End with Best regards,
""",
                "stream": False
            }
        )
        return response.json()["response"].strip()

    except:
        return "AI not connected (start Ollama locally)"

important_df = df[df["Category"] == "IMPORTANT"].copy()

important_df["Reply"] = important_df["Subject"].apply(generate_ai_reply)

# 🔹 Chart
st.subheader("📊 Email Distribution")
st.bar_chart(df["Category"].value_counts())

# 🔹 Tables
st.subheader("📋 All Emails")
st.dataframe(df)

st.subheader("✅ Important Emails")
st.dataframe(important_df[["Subject", "Category"]])

st.subheader("🤖 Suggested Replies")
st.dataframe(important_df[["Subject", "Reply"]])
