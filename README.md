# EmotiAI Support  

**Empowering emotional well-being with AI-driven solutions.**  

## About the Project  
EmotiAI Support is an advanced AI chatbot that acts as a digital therapist, integrating Cognitive Behavioral Therapy (CBT) principles. It recognizes emotional states, provides personalized guidance, and offers empathetic support.  

## Key Objectives  
- Detect and interpret emotional states through text and voice.  
- Deliver expert-level emotional support rooted in CBT.  
- Ensure user privacy and confidentiality.  
- Refer users to professional help when necessary.  

## Technologies Used  
- **Snowflake Cortex Search:** Retrieves mental health and therapy documents.  
- **Mistral LLM (mistral-large2):** Delivers empathetic conversational responses.  
- **Streamlit:** Provides an intuitive user interface.  
- **Retrieval-Augmented Generation (RAG):** Ensures context-rich, evidence-based responses.  

## Features  
- Emotional recognition and adaptive interactions.  
- Expert CBT-based therapeutic advice.  
- Confidential, personalized, and secure support.  
- Professional referrals for complex cases.  

## Prerequisites

- Python version 3.11 or below
  - Download and install Python 3.11 from the official website: [Python Downloads](https://www.python.org/downloads/)
  
## Project Setup

### Step 1: Clone or download the project files

Ensure that you have the following files in your project directory:
- `file.py`
- `requirements.txt`

### Step 2: Set up Python Virtual Environment

1. Navigate to the project directory.
2. Run the following command to create a virtual environment:

for Windows Powershell:
   1) python -m venv .venv 
   2) .venv\Scripts\Activate.ps1

### Step 3: Install all requirements

1. Navigate to the project directory.
2. Run the following command to create a virtual environment:

for Windows Powershell:
   1) pip install -r requirements.txt

## Step 4: Create Database and schema in Snowflake and a Cortex Search service

1. Create a vast collection of Cognitive Behavioural therapy guides and research and create chunks in the database.
2. Refer to this link to create database and search services - https://quickstarts.snowflake.com/guide/ask_questions_to_your_own_documents_with_snowflake_cortex_search/#0

### Step 5: Create .env file and enter your snowflake account details
SNOWFLAKE_USER=<br>
SNOWFLAKE_USER_PASSWORD=<br>
SNOWFLAKE_ACCOUNT=<br>
SNOWFLAKE_DATABASE=<br>
SNOWFLAKE_SCHEMA=<br>
SNOWFLAKE_WAREHOUSE=<br>
SNOWFLAKE_ROLE=<br>
SNOWFLAKE_CORTEX_SEARCH_SERVICE=<br>

### Step 6: streamlit run file.py


