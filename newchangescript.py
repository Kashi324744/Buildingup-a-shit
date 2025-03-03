import streamlit as st
import random
import google.generativeai as genai
import boto3
import pdfkit
import os

# Configure Gemini AI (Use a valid API Key)
genai.configure(api_key="")

# AWS S3 Configuration
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
BUCKET_NAME = ""

MODEL_NAME = "gemini-1.5-pro-001"

def generate_story():
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = "Generate a thrilling, interactive story scenario where the player must make critical decisions. Keep it engaging and suspenseful and think of many different stories do not stick to a single kind of story, it could be a funny story, thriller, murder mystery stories anything but different genre."
    response = model.generate_content(prompt)
    return response.text if response else "Error generating story."

def process_user_action(user_input, chat_history):
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = (
        "This is an interactive game. Continue the narrative based on the player's choices.\n\n"
        "Game so far:\n"
        + "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history]) +
        f"\n\nPlayer: {user_input}\nGame Master:"
    )
    
    response = model.generate_content(prompt)
    return response.text if response else "Error processing action."

def save_webpage_as_pdf(html_content, filename="exported_page.pdf"):
    options = {
        "enable-local-file-access": "",
        "page-size": "A4",
        "encoding": "UTF-8",
        "no-outline": None
    }
    pdfkit.from_string(html_content, filename, options=options)
    return filename

def upload_to_s3(file_name, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_name  

    s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    
    try:
        s3.upload_file(file_name, bucket_name, object_name)
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        return s3_url
    except Exception as e:
        return str(e)

# Streamlit UI
st.set_page_config(page_title="Interactive Thriller", layout="wide")
st.title(" *Build-up a sh**t* ")

if st.button("🎲 New Story"):
    story = generate_story()
    st.session_state.scenario_title = "New Interactive Thriller"
    st.session_state.scenario_description = story
    st.session_state.chat_history = []

if "scenario_title" not in st.session_state:
    story = generate_story()
    st.session_state.scenario_title = "New Interactive Thriller"
    st.session_state.scenario_description = story

st.subheader(st.session_state.scenario_title)
st.write(st.session_state.scenario_description)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("Game Interaction")
chat_container = st.container()
for msg in st.session_state.chat_history:
    chat_container.markdown(f"**{msg['role']}**: {msg['content']}")

user_input = st.text_input("Enter your action:", key="user_input", placeholder="Type here...")

if st.button("🚀 Submit Action") and user_input:
    ai_response = process_user_action(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "You", "content": user_input})
    st.session_state.chat_history.append({"role": "AI", "content": ai_response})
    st.rerun()

if st.button("Export"):
    html_content = f"""
    <h1> ChatLog </h1>
    <h2>{st.session_state.scenario_title}</h2>
    <p>{st.session_state.scenario_description}</p>
    <h3>Game Interaction</h3>
    <ul>
    {''.join([f'<li><b>{msg["role"]}:</b> {msg["content"]}</li>' for msg in st.session_state.chat_history])}
    </ul>
    """
    
    pdf_file = save_webpage_as_pdf(html_content, "game_history.pdf")
    s3_url = upload_to_s3(pdf_file, BUCKET_NAME)
    os.remove(pdf_file)

    if s3_url.startswith("http"):
        st.success("✅ Exported successfully!")
        st.markdown(f"[📂 Download PDF from S3]({s3_url})")
    else:
        st.error(f"❌ Upload failed: {s3_url}")
