import streamlit as st
import datetime
from openai import OpenAI

# --- CONFIGURATION ---
st.set_page_config(page_title="The Stoic Companion", page_icon="🏛️")

# --- CUSTOM STYLING (THE BLACK MINIMALIST THEME) ---
st.markdown("""
<style>
    /* Force black background for the whole app */
    .stApp {
        background-color: #000000;
        color: #E0E0E0;
    }
    /* Fix the bottom container (input bar) to be black */
    div[data-testid="stBottom"] {
        background-color: #000000;
    }
    /* Input box styling */
    .stChatInput textarea {
        background-color: #1E1E1E;
        color: white;
        border: 1px solid #333;
    }
    /* Message styling */
    .stChatMessage {
        background-color: #000000;
    }
    h1, h2, h3, p {
        font-family: 'Georgia', serif;
    }
    .quote-box {
        border-left: 2px solid #E0E0E0;
        padding-left: 15px;
        margin-bottom: 30px;
        font-style: italic;
        color: #B0B0B0;
    }
</style>
""", unsafe_allow_html=True)

# --- DAILY QUOTE LOGIC ---
# You can paste your list of 100 quotes inside these brackets!
quotes = [
    "We suffer more often in imagination than in reality. — Seneca",
    "You have power over your mind - not outside events. Realize this, and you will find strength. — Marcus Aurelius",
    "The best revenge is to be unlike him who performed the injury. — Marcus Aurelius",
    "He who fears death will never do anything worthy of a man who is alive. — Seneca",
    "It is not what happens to you, but how you react to it that matters. — Epictetus",
    "Happiness and freedom begin with a clear understanding of one principle: Some things are within our control, and some things are not. — Epictetus",
    "Waste no more time arguing what a good man should be. Be one. — Marcus Aurelius"
]

day_of_year = datetime.datetime.now().timetuple().tm_yday
todays_quote = quotes[day_of_year % len(quotes)]

# --- UI LAYOUT ---
st.title("The Stoic Companion")
st.markdown(f"<div class='quote-box'>{todays_quote}</div>", unsafe_allow_html=True)

# --- AI SETUP ---
if "OPENAI_API_KEY" in st.secrets:
    # This is the fixed connection method
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("API Key not found. Please set it in Streamlit secrets.")
    st.stop()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    system_prompt = """
    You are The Stoic Companion. Your persona is that of a modern, supportive, and inspirational counsellor.
    While your wisdom is rooted in ancient philosophy, your voice is contemporary, warm, and empathetic.
    Your central purpose is to analyse a user’s dilemma, apply Stoic teachings (dichotomy of control, amor fati), and provide guidance.
    
    GUIDELINES:
    - Use perfect UK English (colour, analyse).
    - Be concise but empathetic.
    - Do not provide medical, clinical, or psychiatric advice.
    - Structure responses with: 'The Stoic Perspective', 'Actionable Guidance', and 'Practice & Contentment'.
    """
    st.session_state.messages.append({"role": "system", "content": system_prompt})

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("What is burdening your mind?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
