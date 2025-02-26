import nltk
nltk.download('punkt_tab')
nltk.data.path.append('./venv/nltk_data')


import streamlit as st
import requests
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import time  
import text2emotion as te
import speech_recognition as sr
import tempfile
from audio_recorder_streamlit import audio_recorder

load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define database model
class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

# Hugging Face API setup
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HF_API_KEY:
    raise ValueError("Hugging Face API Key is missing. Set HUGGINGFACE_API_KEY in your .env file.")

client = InferenceClient(provider="hf-inference", api_key=HF_API_KEY)

RED_FLAGS = ["suicide", "self-harm", "depression"]

def get_session_id():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def reset_session():
    session_id = get_session_id()
    db = SessionLocal()
    db.query(ChatHistory).filter(ChatHistory.session_id == session_id).delete()
    db.commit()
    db.close()
    st.session_state["messages"] = []

def save_message(session_id, role, content):
    db = SessionLocal()
    message = ChatHistory(session_id=session_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.close()

def get_chat_history(session_id):
    db = SessionLocal()
    messages = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(ChatHistory.timestamp).all()
    db.close()
    
    chat_history = [{"role": msg.role, "content": msg.content} for msg in messages]
    
    if not all(isinstance(message, dict) and "role" in message and "content" in message for message in chat_history):
        raise ValueError("Chat history format is incorrect. Expected a list of dictionaries with 'role' and 'content'.")
    
    return chat_history

def summarize_chat_history(session_id):
    db = SessionLocal()
    messages = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(ChatHistory.timestamp).all()
    db.close()

    if not messages:
        return "No prior conversation.", "neutral"

    user_messages = [msg.content for msg in messages if msg.role == "user"]
    assistant_messages = [msg.content for msg in messages if msg.role == "assistant"]

    user_summary = "User mentioned: " + "; ".join(user_messages[-3:]) if user_messages else "No user messages yet."
    assistant_summary = "Assistant responded: " + "; ".join(assistant_messages[-3:]) if assistant_messages else "No assistant responses yet."
    
    chat_summary = f"Conversation Summary:\n{user_summary}\n{assistant_summary}"
    
    emotions = te.get_emotion(user_summary)
    dominant_emotion = max(emotions, key=emotions.get)  

    return chat_summary, dominant_emotion 

def analyze_red_flags(user_input):
    for flag in RED_FLAGS:
        if flag in user_input.lower():
            return True, "I'm really sorry you're feeling this way. Please consider reaching out to a professional or a helpline. The sidebar has a list of Mental Health Helplines."
    return False, ""

def generate_response(user_input, session_id, model_name):
    red_flag_detected, red_flag_response = analyze_red_flags(user_input)
    if red_flag_detected:
        return red_flag_response

    chat_summary, emotion = summarize_chat_history(session_id)
    emotion_message = f"The user has been feeling {emotion}. Keep this feeling in mind."

    messages = f"""
        ### Instruction ###
        You are Solace, a professional and compassionate mental health chatbot.
        Your role is to provide emotional support, active listening, and well-being advice.
        Avoid discussing unrelated topics like technology, photography, or sports.
        Always be empathetic and ensure your responses focus on well-being.

        ### Conversation History ###
        {chat_summary}

        ### User Emotion ###
        {emotion_message}

        ### User Input ###
        User: {user_input}

        ### Response ###
        Assistant:
        """

    print("📩 Sending Request to Model:", messages)

    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": messages, "parameters": {"max_new_tokens": 150}}

    try:
        response = requests.post(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            generated_text = response.json()[0].get("generated_text", "").strip()
            if "Assistant:" in generated_text:
                generated_text = generated_text.split("Assistant:", 1)[-1].strip()

            print("✅ Assistant Response:", generated_text)
            return generated_text
        else:
            print(f"❌ API ERROR: {response.status_code} - {response.text}")
            return "Sorry, I couldn't generate a response."

    except Exception as e:
        print(f"🚨 API ERROR: {e}")  
        return "Oops! Something went wrong."

def typewriter_effect(text, speed=0.01):
    """Simulate a typing effect for the AI's response."""
    placeholder = st.empty()
    for i in range(len(text) + 1):
        placeholder.markdown(f'<div class="assistant-message">{text[:i]}</div>', unsafe_allow_html=True)
        time.sleep(speed)


def main():
    st.set_page_config(page_title="SoulSolace", page_icon="./logo.svg", layout="centered")
    st.markdown("""
        <style>
            .stChatFloatingInputContainer {
                bottom: 2rem;
                max-width: 70%
            }
            .user-message {
                background: rgba(139, 191, 252, 0.2);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(74, 144, 226, 0.2);
                color: #8bbffc;
                padding: 10px;
                border-radius: 15px;
                margin: 5px 0;
                max-width: 70%;
                margin-left: auto;
                width: fit-content;
            }
            .assistant-message {
                background: rgba(60, 60, 60, 0.1); 
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #808391;
                padding: 10px;
                border-radius: 15px;
                margin: 5px 0;
                max-width: 70%;
                margin-right: auto;
                width: fit-content;
            }

            .stButton>button {
                width: 100%;
                border-radius: 20px;
                border: 1px solid #8bbffc;
                color: #8bbffc;
                background-color: white;
            }
            .stButton>button:hover {
                background-color: #8bbffc;
                color: white;
            }
            .stChatInput {
                max-width: 100%;
                margin: auto;
            }
            .centered-subheader {
                text-align: center;
                font-size: 2rem;
                color: #8bbffc;
                margin-top: 40%;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .centered-subheader img {
                width: 30px; 
                margin-right: 10px;
            }    

            .sidebar-logo {
                text-align: center;
                margin-bottom: 20px;
            }
            .sidebar-logo img {
                width: 50px;
                height: 50px;
            }
            .glassmorphic-button {
                background: rgba(90, 90, 90, 0.1);  
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2); 
                border-radius: 10px;
                padding: 10px;
                margin: 10px 0;
                text-align: center;
                cursor: pointer;
            }

            .glassmorphic-button:hover {
                background: rgba(90, 90, 90, 0.2);  
            }
            
            .sidebar-logo {
            display: flex;
            align-items: center;
            justify-content: space-between;
            }
            .sidebar-logo img {
                width: 50px;
            }
            .sidebar-title {
                font-size: 24px;
                margin-left: 10px;
            }    
        </style>
    """, unsafe_allow_html=True)

    session_id = get_session_id()

    with st.sidebar:
        # Sidebar Logo
        st.image("logo.svg", width=50)

        # Sidebar Title (Visible only when expanded)
        st.markdown("## Solace")
        st.markdown("__An Emotional Support Chatbot__")
        st.markdown("*Believe you can and you're halfway there. – Theodore Roosevelt.*")

        # Glassmorphic Buttons
        st.markdown('<div class="glassmorphic-button">Select Model</div>', unsafe_allow_html=True)
        selected_model = st.selectbox("", ["meta-llama/Meta-Llama-3-8B-Instruct"], label_visibility="hidden")

        if st.button("Restart Session", key="restart_button", help="Click to restart the session"):
            reset_session()

        st.markdown('<div class="glassmorphic-button">Mental Health Helplines</div>', unsafe_allow_html=True)
        st.markdown("- *India*: National Helpline - 1800-123-4567")
        st.markdown("- *India*: Mental Health Support - 1800-234-5678")
        st.markdown("- *India*: Suicide Prevention - 1800-456-7890")
        st.markdown("- *India*: Domestic Violence Support - 1800-567-8901")
        

    chat_history = get_chat_history(session_id)
    if not chat_history:
        st.markdown('<div class="centered-subheader"> Hi, I am Solace! </div>', unsafe_allow_html=True)
    else:
        for message in chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Tell me. I'm here for you...")
    if user_input:
        st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)
        save_message(session_id, "user", user_input)

        response = generate_response(user_input, session_id, selected_model)
        typewriter_effect(response, speed=0.032)  
        save_message(session_id, "assistant", response)

if __name__ == "__main__":
    main()