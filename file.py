import streamlit as st
import uuid
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os
import json
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
    session_id = Column(String, primary_key=True)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

# Get Hugging Face API key
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
if not HF_API_KEY:
    raise ValueError("Hugging Face API Key is missing. Set HUGGINGFACE_API_KEY in your .env file.")

# Use Hugging Face Inference API instead of local model
# client = InferenceClient(model="mistralai/Mistral-7B-v0.1", token=HF_API_KEY)
# print(client)  # Debugging: Ensure the client is initialized

client = InferenceClient(
	provider="hf-inference",
	api_key=HF_API_KEY
)

messages = [
	{
		"role": "user",
		"content": "What is the capital of France?"
	}
]

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", 
	messages=messages, 
	max_tokens=500
)

print(completion.choices[0].message)

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

# Generate response using Hugging Face API with error handling
def generate_response(user_input, session_id):
    red_flag_detected, red_flag_response = analyze_red_flags(user_input)
    if red_flag_detected:
        return red_flag_response

    chat_history = get_chat_history(session_id)
    prompt_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[-5:]])
    prompt = f"{prompt_context}\nUser: {user_input}\nAI:"
    print(prompt)

    try:
        # Call Hugging Face API for inference
        response = client.text_generation(prompt, max_new_tokens=100, return_full_text=False)

        # Debugging: Print response in logs
        print("Raw API Response:", response)

        # Handle case where response is empty
        if not response:
            st.error("Error: Received an empty response from the Hugging Face API.")
            return "I'm having trouble generating a response right now. Please try again later."

        # Ensure response is extracted properly
        if isinstance(response, dict) and "generated_text" in response:
            return response["generated_text"].strip()

        return response.strip()

    except Exception as e:
        error_message = f"Error in response generation: {str(e)}"
        print(error_message)  # Logs error
        st.error(error_message)  # Show error in Streamlit UI
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

    if user_input := st.chat_input("How can I support you today?"):
        with st.chat_message("user"):
            st.markdown(user_input)
        save_message(session_id, "user", user_input)
        
        with st.chat_message("assistant"):
            response = generate_response(user_input, session_id)
            print("Generated Response:", response)  # Debugging
            st.markdown(response)
        save_message(session_id, "assistant", response)

if __name__ == "__main__":
    main()
