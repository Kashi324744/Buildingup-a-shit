import streamlit as st
import random
import google.generativeai as genai

# Configure Gemini AI
genai.configure(api_key="")  # ⚠ Replace with actual key

MODEL_NAME = "gemini-1.5-pro-001"

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
    """Picks a random scenario from the list."""
    scenario = random.choice(SCENARIOS)
    return scenario["title"], scenario["description"]

def process_user_action(user_input, chat_history):
    """Generates AI-driven response, continuing the story dynamically."""
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

# Streamlit UI Setup
st.set_page_config(page_title="Interactive Thriller Game", layout="wide")
st.title("🌀 *Interactive Thriller Game* 🌀")

# New Scenario Button
if st.button("🎲 New Story"):
    title, description = get_random_scenario()
    st.session_state.scenario_title = title
    st.session_state.scenario_description = description
    st.session_state.chat_history = []

# Scenario Initialization
if "scenario_title" not in st.session_state:
    title, description = get_random_scenario()
    st.session_state.scenario_title = title
    st.session_state.scenario_description = description

st.subheader(st.session_state.scenario_title)
st.write(st.session_state.scenario_description)

# Chat-based Interaction
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.subheader("Game Interaction")
user_input = st.text_input("Enter your action:", key="user_input")

if st.button("🚀 Submit Action", key="submit_action") and user_input:
    ai_response = process_user_action(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append({"role": "You", "content": user_input})
    st.session_state.chat_history.append({"role": "AI", "content": ai_response})

# Display Chat History
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
