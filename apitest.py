from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HF_API_KEY:
    raise ValueError("API Key is missing!")

print(f"Loaded API Key: {HF_API_KEY[:5]}...")  # Print first few chars for validation

client = InferenceClient(model="mistralai/Mistral-7B-v0.1", token=HF_API_KEY)

try:
    print("Sending request to Hugging Face API...")
    response = client.text_generation("Hello, how are you?", max_new_tokens=100)
    print("API Response:", response)

except Exception as e:
    print("API Error:", e)
