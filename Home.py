import streamlit as st
from PIL import Image

def main():
    st.set_page_config(page_title="SoulSolace", page_icon="logo.svg", layout="centered")
    
    st.markdown(
        """
        <style>
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                height: 80vh;
            }
            .center-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                width: 100%;
            }
            .options-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
            }
            .option-card {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 30px;
                width: 250px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .option-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
            }
            .option-button {
                border-radius: 10px;
                border: none;
                background-color: #8bbffc;
                color: white;
                padding: 12px 20px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
                text-decoration: none;
                display: inline-block;
            }
            .option-button:hover {
                background-color: #6498db;
            }
            @media (max-width: 768px) {
                .options-container {
                    flex-direction: column;
                    align-items: center;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    
    with st.container():  
        col1, col2, col3 = st.columns([1, 2, 1])    
        with col2:
            st.image("logo.svg", width=80)

    st.markdown(
        """
        <div class="center-container">
            <h1 style="color: #8bbffc; font-weight: 500;"> Hi, I am Solace! </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Options Section
    st.markdown(
        """
        <div class='container'>
            <p>Choose how you want to interact:</p>
            <div class='options-container'>
                <div class='option-card'>
                    <h4>⌨️ Text Chat</h4>
                    <p>Chat with me, and see what I can do for you.</p>
                    <a href='/Text_Chat' class='option-button'>Start</a>
                </div>
                <div class='option-card'>
                    <h4>🎙️ Voice Chat</h4>
                    <p>Talk to me for an interactive experience.</p>
                    <a href='/Voice_Chat' class='option-button'>Start</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
