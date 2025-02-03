

# Solace - AI-Powered Chatbot

*Solace* is an AI-powered chatbot designed to provide users with personalized and engaging conversations. Using a combination of advanced NLP models like Meta's LLaMA, sentiment analysis tools, and speech recognition, Solace offers a seamless conversational experience with context-aware and emotion-sensitive responses. It supports both text and voice-based interactions and is fully dockerized and deployed on AWS for scalability and reliability.

## Features
- **Contextual Conversations**: Powered by **Meta LLaMA** for intelligent response generation.
- **Emotion-Aware**: Detects emotions through **Text2Emotion** and adapts responses accordingly.
- **Voice Interaction**: Supports **Speech-to-Text** and **Speech Recognition** for voice-based interactions.
- **Cloud Deployment**: Dockerized and hosted on **AWS** for scalability and performance.
- **Easy Setup**: Quick setup using **Docker**, **Python dependencies**, and **environment variables**.


## Installation

## Prerequisites  
Before running the project, make sure you have:  
- **[Docker](https://docs.docker.com/get-docker/)** installed and running.  
- **[Python 3.10](https://www.python.org/downloads/)** installed. 

### Local Setup
Follow the steps below to set up Solace on your local machine:

###  1. Clone the Repository  

```bash
git clone https://github.com/your-repo/SoulSolace.git  
cd SoulSolace  
```

###  2. Create a Virtual Environment (optional but recommended)  

###  On Linux/macOS  

```bash
python3 -m venv venv  
source venv/bin/activate 
``` 

###  On Windows (Run in PowerShell)  

```bash
python -m venv venv  
venv\Scripts\activate  
```

###  3. Install Dependencies  

```bash
pip install -r requirements.txt  
```

###  Run the Application  

###  1. Start the Streamlit application  

```bash
streamlit run file.py  
```

###  Access the Chatbot

Visit http://localhost:8501 to interact with the chatbot.

---

## Docker Setup

If you want to run the application using Docker, follow the steps below:

###  1. Clone the Repository  

```bash
git clone https://github.com/your-repo/SoulSolace.git  
cd SoulSolace 
```


### 2. Build the Docker Image:

   ```bash
   sudo docker-compose build
   ```

### 3. Run the containers:

   ```bash
   sudo docker-compose up -d
   ```

### 4. Access the app:

   The app will be available at http://localhost:8501.

---

## Tech Stack

1. *Streamlit & HTML/CSS*: Provides a fast and interactive web UI for chatbot interactions. Custom HTML/CSS ensures a polished user experience.
   
2. *Hugging Face Transformers*: Utilized for powerful NLP tasks like response generation and understanding. Hugging Face simplifies the integration of pre-trained models like Meta LLaMA.

3. *Text2Emotion*: Detects emotions from user input to enable personalized, emotion-sensitive responses from the chatbot.

4. *Speech-to-Text & Speech Recognition*: Allows users to interact with the chatbot using voice commands, making it more accessible and engaging.

5. *Meta LLaMA Model*: A highly efficient and advanced model for natural language processing, enabling context-aware, dynamic conversations with users.

6. *PostgreSQL & SQLAlchemy*: Used for structured storage of user data and conversation history, ensuring quick retrieval and consistency.

7. *Docker*: Docker ensures easy deployment and scalability.

---

## Contribution Guidelines

We welcome contributions to Solace! Here’s how you can contribute:

1. *Fork the repository* and clone it locally.

2. *Create a new branch* for your feature or bugfix:

   bash
   git checkout -b feature/your-feature-name
   

3. *Write tests* for any new functionality or fixes.

4. *Ensure code follows PEP 8* guidelines. Use black for code formatting and flake8 for linting.

5. *Commit changes* with descriptive messages:

   bash
   git commit -m "feat: add new feature"
   

6. *Push changes* to your fork:

   bash
   git push origin feature/your-feature-name
   

7. *Open a Pull Request* to the main repository.

8. *Review process*: Once your PR is reviewed, be ready to make necessary changes and improvements based on feedback.

---

