import streamlit as st
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://chatuser:password@localhost/amdocschatbot")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define database model
class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Fixed primary key
    session_id = Column(String, nullable=False, index=True)  # No primary key
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
    return [{"role": msg.role, "content": msg.content} for msg in messages]

def analyze_red_flags(user_input):
    for flag in RED_FLAGS:
        if flag in user_input.lower():
            return True, "I'm really sorry you're feeling this way. Please consider reaching out to a professional or a helpline. The sidebar has a list of Mental Health Helplines."
    return False, ""

def generate_response(user_input, session_id):
    red_flag_detected, red_flag_response = analyze_red_flags(user_input)
    if red_flag_detected:
        return red_flag_response

    messages = [{"role": "user", "content": user_input}]

    try:
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", 
            messages=messages, 
            max_tokens=500
        )

        if completion.choices:
            return completion.choices[0].message.content.strip()
        else:
            return "Sorry, I couldn't generate a response."

    except Exception as e:
        error_message = f"Error in response generation: {str(e)}"
        print(error_message)
        st.error(error_message)
        return "Oops! Something went wrong. Please try again later."

def main():
    st.title(":speech_balloon: EmotiAI Support Chatbot")
    st.markdown("Welcome to the Emotional Health Support Chatbot. ❤️")

    session_id = get_session_id()
    
    with st.sidebar:
        st.selectbox("Select your model:", ["DeepSeek-R1-Distill-Qwen-32B"])
        if st.button("Restart Session"):
            reset_session()
        st.markdown("### 📞 Mental Health Helplines")
        st.markdown("- *India*: AASRA - 91-9820466726")
        st.markdown("- *USA*: National Suicide Prevention Lifeline - 988")

    chat_history = get_chat_history(session_id)
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("How can I support you today?")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        save_message(session_id, "user", user_input)
        
        with st.chat_message("assistant"):
            response = generate_response(user_input, session_id)
            st.markdown(response)
        save_message(session_id, "assistant", response)

if __name__ == "__main__":
    main()
