import streamlit as st
import random
import google.generativeai as genai
import boto3
import pdfkit
import os

# Configure Gemini AI (Use a valid API Key)
genai.configure(api_key="Gemini_API_Key")

# AWS S3 Configuration
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
BUCKET_NAME = "rawemailbucket1"

MODEL_NAME = "gemini-1.5-pro-001"

# Scenarios
SCENARIOS = [
    {
        "title": "🚨 School Attack – Survive or Die!",
        "description": (
            "Gunshots echo through the halls, the lights flicker, and fear grips your heart. "
            "You're trapped in your school as chaos unfolds. No one knows where the shooter is. "
            "You have no weapon, no backup, just your wits.\n\n"
            "*What’s your first move?*"
        ),
    },
    {
        "title": "⚡ Mystery Superpower – But Which One?",
        "description": (
            "You wake up in your room, but something feels... off. As you stretch, the lamp beside you "
            "suddenly shatters, even though you didn’t touch it. You feel an unfamiliar energy in your veins.\n\n"
            "*You have a superpower, but you don’t know what it is. How do you test it?*"
        ),
    },
    {
        "title": "👀 Reverse Gender Awakening",
        "description": (
            "You wake up feeling strange. Something is wrong—your hands, your voice, even your reflection in the mirror. "
            "You are no longer you. Somehow, overnight, you've become the opposite gender.\n\n"
            "*How do you react? What’s the first thing you do?*"
        ),
    },
    {
        "title": "🔪 Murder Mystery – You’re the Prime Suspect",
        "description": (
            "The police have just barged into your apartment. Bloodstains cover your hands, and a lifeless body lies on the floor. "
            "You don’t remember anything. Your head throbs, your heart races. The cops are shouting at you.\n\n"
            "*Do you confess, run, or try to recall what happened?*"
        ),
    },
    {
        "title": "⏳ Trapped in a Time Loop",
        "description": (
            "It’s happening again. The same morning, the same street, the same people… but wait. You died last night, didn’t you? "
            "You remember it clearly—being hit by a car. But now you’re back at the start of your day.\n\n"
            "*What’s your next move?*"
        ),
    },
]

def get_random_scenario():
    scenario = random.choice(SCENARIOS)
    return scenario["title"], scenario["description"]

def process_user_action(user_input, chat_history):
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = (
        "This is an immersive interactive thriller game. You are the Game Master, and the player "
        "experiences the story in real-time. Based on their actions, continue the narrative with suspense, "
        "thrills, and unexpected twists. Keep responses engaging and cinematic.\n\n"
        "Game so far:\n"
        + "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history]) +
        f"\n\nPlayer: {user_input}\nGame Master:"
    )
    
    response = model.generate_content(prompt)
    return response.text if response else "Error processing action."

def analyze_game(chat_history):
    """Rates the player's performance based on their choices."""
    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = (
        "Analyze the player's decisions in this interactive thriller game. "
        "1. Rate their instincts (0-10).\n"
        "2. Give feedback on smart or risky choices.\n"
        "3. Suggest better actions they could have taken.\n\n"
        "Game so far:\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
    )

    response = model.generate_content(prompt)
    return response.text if response else "Error analyzing game."

def save_webpage_as_pdf(html_content, filename="exported_page.pdf"):
    """Saves the entire webpage as a PDF using pdfkit."""
    options = {
        "enable-local-file-access": "",
        "page-size": "A4",
        "encoding": "UTF-8",
        "no-outline": None
    }
    pdfkit.from_string(html_content, filename, options=options)
    return filename

def upload_to_s3(file_name, bucket_name, object_name=None):
    """Uploads a file to S3 and returns the download link."""
    if object_name is None:
        object_name = file_name  # S3 object name

    s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    try:
        s3.upload_file(file_name, bucket_name, object_name)
        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        return s3_url
    except Exception as e:
        return str(e)

# Streamlit UI
st.set_page_config(page_title="Interactive Thriller", layout="wide")
st.title("🌀 *Build-Up Sh*t* 🌀")

# New Scenario Button
if st.button("🎲 New Story"):
    title, description = get_random_scenario()
    st.session_state.scenario_title = title
    st.session_state.scenario_description = description
    st.session_state.chat_history = []

# Initialize scenario
if "scenario_title" not in st.session_state:
    title, description = get_random_scenario()
    st.session_state.scenario_title = title
    st.session_state.scenario_description = description

st.subheader(st.session_state.scenario_title)
st.write(st.session_state.scenario_description)

# Ensure chat history is initialized
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages
st.subheader("Game Interaction")
chat_container = st.container()
for msg in st.session_state.chat_history:
    chat_container.markdown(f"**{msg['role']}**: {msg['content']}")

# User input
user_input = st.text_input("Enter your action:", key="user_input", placeholder="Type here and press Enter...")

if st.button("🚀 Submit Action") and user_input:
    ai_response = process_user_action(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "You", "content": user_input})
    st.session_state.chat_history.append({"role": "AI", "content": ai_response})
    st.rerun()

# Submit button at the bottom for better UX
st.markdown("<br><br>", unsafe_allow_html=True)

# Game Analysis Feature
if st.button("📊 Analyze My Choices"):
    if st.session_state.chat_history:
        analysis = analyze_game(st.session_state.chat_history)
        st.subheader("Game Analysis & Rating")
        st.write(analysis)
    else:
        st.warning("Play the game first before analyzing!")

        
# Export and Upload PDF Button
if st.button("Export"):
    html_content = f"""
    <h1>🌀 Game 🌀</h1>
    <h2>{st.session_state.scenario_title}</h2>
    <p>{st.session_state.scenario_description}</p>
    <h3>Game Interaction</h3>
    <ul>
    {''.join([f'<li><b>{msg["role"]}:</b> {msg["content"]}</li>' for msg in st.session_state.chat_history])}
    </ul>
    """
    
    pdf_file = save_webpage_as_pdf(html_content, "game_history.pdf")
    s3_url = upload_to_s3(pdf_file, BUCKET_NAME)
    os.remove(pdf_file)  # Cleanup

    if s3_url.startswith("http"):
        st.success("✅ Exported successfully!")
        st.markdown(f"[📂 Download PDF from S3]({s3_url})")
    else:
        st.error(f"❌ Upload failed: {s3_url}")

for msg in st.session_state.chat_history:
    st.write(f"{msg['role']}:** {msg['content']}")

# Submit button at the bottom for better UX
st.markdown("<br><br>", unsafe_allow_html=True)

# Game Analysis Feature
if st.button("📊 Analyze My Choices"):
    if st.session_state.chat_history:
        analysis = analyze_game(st.session_state.chat_history)
        st.subheader("Game Analysis & Rating")
        st.write(analysis)
    else:
        st.warning("Play the game first before analyzing!")
