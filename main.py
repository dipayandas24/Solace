import streamlit as st
from PIL import Image

def main():
    st.set_page_config(page_title="SoulSolace", page_icon="./logo.svg", layout="centered")
    
    st.markdown("""
        <style>
            .center-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 80vh;
                text-align: center;
            }
            .button-container {
                display: flex;
                gap: 20px;
                margin-top: 30px;
            }
            .stButton>button {
                border-radius: 15px;
                border: 1px solid #8bbffc;
                color: #8bbffc;
                background-color: white;
                padding: 10px 20px;
                font-size: 18px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .stButton>button:hover {
                background-color: #8bbffc;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Logo and Title
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <img src='./logo.svg' width='80'>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #8bbffc;'>Welcome to SoulSolace</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Your Personal Mental Health Companion</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='center-container'>
        <p>Choose how you want to interact:</p>
        <div class='button-container'>
            <a href='/text_chat' target='_self'><button>📝 Text Chat</button></a>
            <a href='/voice_chat' target='_self'><button>🎙️ Voice Chat</button></a>
        </div>
    </div>
""", unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()