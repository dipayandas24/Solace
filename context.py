import streamlit as st
import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

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

# Red flags
RED_FLAGS = ["suicide", "self-harm", "depression"]

# Helper functions

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
    
    # Check if the chat history has the correct format
    if not all(isinstance(message, dict) and "role" in message and "content" in message for message in chat_history):
        raise ValueError("Chat history format is incorrect. Expected a list of dictionaries with 'role' and 'content'.")
    
    return chat_history

def summarize_chat_history(session_id):
    db = SessionLocal()
    messages = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(ChatHistory.timestamp).all()
    db.close()

    if not messages:
        return "No prior conversation history."

    user_messages = [msg.content for msg in messages if msg.role == "user"]
    assistant_messages = [msg.content for msg in messages if msg.role == "assistant"]

    user_summary = "User mentioned: " + "; ".join(user_messages[-3:]) if user_messages else "No user messages yet."
    assistant_summary = "Assistant responded: " + "; ".join(assistant_messages[-3:]) if assistant_messages else "No assistant responses yet."

    return f"Conversation Summary:\n{user_summary}\n{assistant_summary}"

def analyze_red_flags(user_input):
    for flag in RED_FLAGS:
        if flag in user_input.lower():
            return True, "I'm really sorry you're feeling this way. Please consider reaching out to a professional or a helpline. The sidebar has a list of Mental Health Helplines."
    return False, ""

def generate_response(user_input, session_id):
    red_flag_detected, red_flag_response = analyze_red_flags(user_input)
    if red_flag_detected:
        return red_flag_response

    # Get chat summary to provide context
    chat_summary = summarize_chat_history(session_id)

    # Ensure chat_summary is a string
    if not isinstance(chat_summary, str):
        raise TypeError(f"Expected a string, got {type(chat_summary)}")

    messages = [
        {"role": "system", "content": "You are a mental health support chatbot. Keep responses empathetic and relevant."},
        {"role": "system", "content": chat_summary},  # Add chat summary as context
        {"role": "user", "content": user_input}
    ]

    try:
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
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

    # Display chat history
    chat_history = get_chat_history(session_id)
    for message in chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input and generate a response
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
