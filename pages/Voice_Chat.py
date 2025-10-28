import nltk
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('brown', quiet=True)
nltk.download('wordnet', quiet=True)
# nltk.data.path.append('./venv/nltk_data')


import streamlit as st
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from nrclex import NRCLex
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time  
import speech_recognition as sr
import tempfile
from audio_recorder_streamlit import audio_recorder

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing. Set it in your .env file for PostgreSQL connection.")
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

from sqlalchemy.exc import IntegrityError
try:
    Base.metadata.create_all(engine)
except IntegrityError:
    pass

# Gemini (Google Generative AI) setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API Key is missing. Set GEMINI_API_KEY in your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

RED_FLAGS = ["suicide", "self-harm", "die", "dying", "end my life"]

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
    return [{"role": msg.role, "content": msg.content} for msg in messages]

def summarize_chat_history(session_id,user_input):
    """Summarizes the last few messages (excluding the latest user input) and extracts user emotions."""
    db = SessionLocal()
    messages = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(ChatHistory.timestamp).all()
    db.close()

    user_messages = [msg.content for msg in messages if msg.role == "user"]
    if user_messages:
        user_messages = user_messages[:-1]

    user_summary = "; ".join(user_messages[-3:]) if user_messages else "No user messages yet. Start a conversation!"
    chat_summary = f"User's last few messages: {user_summary}"

    # Aggregate emotions from all user messages in history using NRCLex
    emotion_scores = {}
    for msg in user_messages:
        text_obj = NRCLex(msg)
        for emotion, score in text_obj.raw_emotion_scores.items():
            emotion_scores[emotion] = emotion_scores.get(emotion, 0) + score
    # If no user messages, fallback to current input
    if not user_messages:
        text_obj = NRCLex(user_input)
        emotion_scores = text_obj.raw_emotion_scores
    dominant_emotion = max(emotion_scores, key=emotion_scores.get) if emotion_scores else "neutral"

    return chat_summary, dominant_emotion

def analyze_red_flags(user_input):
    flag1 = "fired"
    if(flag1 in user_input.lower()):
        return True, "I'm really sorry to hear that. I know this must be an incredibly tough moment for you, and it's okay to feel upset. But please remember—this does not define your worth or your abilities. Many successful people have faced setbacks like this and used them as a turning point for something even better. Take some time to process your emotions, but also remind yourself that this could be the start of a new opportunity. You have skills, experience, and resilience, and the right door will open for you. When you're ready, update your resume, reach out to your network, and explore new possibilities. You are stronger than this situation, and you will rise again. If you need to talk, I’m here for you. Sending you strength and support!"
    for flag in RED_FLAGS:
        if flag in user_input.lower():
            return True, "I'm really sorry you're feeling this way. Please consider reaching out to a professional or a helpline. \n Contact: Mental Health Support - 1800-234-5678"
    return False, ""

# Removed Hugging Face InferenceClient - using Google Gemini instead

def generate_response(user_input, session_id):
    """Generates a meaningful response using Hugging Face Inference API with proper formatting."""

    red_flag_detected, red_flag_response = analyze_red_flags(user_input)
    if red_flag_detected:
        return red_flag_response
    chat_summary, dominant_emotion = summarize_chat_history(session_id,user_input)

    messages = [
        {
            "role": "user", 
            "content": f"{user_input}. I am feeling {dominant_emotion}. Behave like an emotional support chatbot and tailor your reply accordingly. My previous interaction with you was {chat_summary}. Consider the previous interaction while replying. Please keep your reply crisp, concise, and supportive—no more than 5-7 sentences."
        },
    ]

    try:
        model_name = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat()

        response = chat.send_message(messages[0]["content"], stream=False)

        generated_text = getattr(response, "text", None)
        if not generated_text:
            generated_text = str(response)

        if not generated_text:
            generated_text = "I'm here for you. Please tell me more about how you're feeling."

        return generated_text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def handle_audio_input():
    """Capture voice input, convert to text using Google Speech Recognition."""
    audio_data = audio_recorder()

    if audio_data:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_data)
            temp_audio_file.close()

            recognizer = sr.Recognizer()
            audio_file = sr.AudioFile(temp_audio_file.name)

            with audio_file as source:
                audio = recognizer.record(source)

            try:
                user_input = recognizer.recognize_google(audio)  # Convert audio to text
                return user_input
            except sr.UnknownValueError:
                st.error("Sorry, I couldn't understand the audio.")
                return None
            except sr.RequestError as e:
                st.error(f"Speech recognition service error: {e}")
                return None
    return None

def typewriter_effect(text, speed=0.02):
    """Display AI response with a typing effect."""
    placeholder = st.empty()
    for i in range(len(text) + 1):
        placeholder.markdown(f'<div class="assistant-message">{text[:i]}</div>', unsafe_allow_html=True)
        time.sleep(speed)

def main():
    st.set_page_config(page_title="SoulSolace Voice Chat", page_icon="./logo.svg", layout="centered")

    st.markdown("""
        <style>
            .user-message {
                background: rgba(139, 191, 252, 0.2);
                padding: 10px;
                border-radius: 15px;
                max-width: 70%;
                margin-left: auto;
                width: fit-content;
                color: #8bbffc;
            }
            .assistant-message {
                background: rgba(60, 60, 60, 0.1); 
                padding: 10px;
                border-radius: 15px;
                max-width: 70%;
                margin-right: auto;
                width: fit-content;
                color: #808391;
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

        if st.button("Restart Session", key="restart_button", help="Click to restart the session"):
            reset_session()

        st.markdown('<div class="glassmorphic-button">Mental Health Helplines</div>', unsafe_allow_html=True)
        st.markdown("- *India*: National Helpline - 1800-123-4567")
        st.markdown("- *India*: Mental Health Support - 1800-234-5678")
        st.markdown("- *India*: Suicide Prevention - 1800-456-7890")
        st.markdown("- *India*: Domestic Violence Support - 1800-567-8901")
        
    st.markdown('<h1 style="color: #8bbffc; font-weight: 500;"> Hi, I am Solace! </h1>', unsafe_allow_html=True)

    st.markdown("**Let's actually talk the way we like the most**")

    user_input = handle_audio_input()

    # Display previous chat history
    chat_history = get_chat_history(session_id)
    for msg in chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)

    if user_input:
        save_message(session_id, "user", user_input)
        st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)

        response = generate_response(user_input, session_id)
        typewriter_effect(response, speed=0.032)
        save_message(session_id, "assistant", response)

if __name__ == "__main__":
    main()
