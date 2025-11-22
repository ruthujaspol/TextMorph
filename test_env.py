from dotenv import load_dotenv
import os

# Use raw string path
env_path = r"J:\Infosys\TextMorph\src\.env"
print(f"Loading .env from: {env_path}")

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("HF_API_KEY")
print("HF_API_KEY:", api_key)
