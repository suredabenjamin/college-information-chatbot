import streamlit as st
from google import genai

# ---------------------------
# Config
# ---------------------------
API_KEY = ""  # paste your API key here
MODEL = "gemini-3.6-flash"
BEN_FILE = "tec document.txt"

st.set_page_config(page_title="TEC Info Chatbot", page_icon="🎓")
st.title("🎓 Thamirabharani Engineering College - Info Chatbot")

# ---------------------------
# Load knowledge base (ben)
# ---------------------------
@st.cache_data
def load_ben(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

ben = load_ben(BEN_FILE)

# ---------------------------
# Build system prompt
# ---------------------------
system_prompt = f"""
You are Thamirabharani Engineering College information chatbot. Your job is to
provide answers to the questions asked by students in a polite manner.
If a question is out of the given information (ben), say you don't have that
information. Only refer to the ben below and provide your response based on it.

{ben}
"""

# ---------------------------
# Initialize client + chat session (once per session)
# ---------------------------
@st.cache_resource
def init_chat():
    client = genai.Client(api_key=API_KEY)
    chat = client.chats.create(
        model=MODEL,
        config={"system_instruction": system_prompt},
    )
    return chat

chat = init_chat()

# ---------------------------
# Session state for chat history (UI display)
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
# Chat input
# ---------------------------
user_input = st.chat_input("Ask a question about the college...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat.send_message(user_input)
                answer = response.text
            except Exception as e:
                answer = f"Sorry, something went wrong: {e}"
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})