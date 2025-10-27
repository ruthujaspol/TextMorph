import os 
import requests 
from dotenv import load_dotenv

class Paraphraser:
    """
    Paraphrasing using GROQ API with LLaMA 3.1 models.
    Recommended models:
    - llama-3.1-8b-instant (fast)
    - llama-3.1-70b-versatile (high quality)
    """

    def __init__(self, model_name="llama-3.1-8b-instant"):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env")

        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model_name = model_name

    def paraphrase(self, text, num_return_sequences=3):
        """
        Generate paraphrased versions of input text using GROQ API.
        """
        if not text.strip():
            return ["⚠️ Please provide valid text."]

        prompt = (
            f"Paraphrase the following text in natural English. "
            f"Provide {num_return_sequences} unique variations as numbered points (1., 2., etc.):\n\n{text}"
        )

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful AI that paraphrases text naturally and clearly."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.9,
            "max_tokens": 1000
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                text_response = data["choices"][0]["message"]["content"]
                
                # Parse numbered points
                lines = []
                for line in text_response.split("\n"):
                    line = line.strip()
                    
                    # Keep lines that start with numbers (1., 2., etc.)
                    if line and any(line.startswith(f"{i}.") for i in range(1, 10)):
                        lines.append(line)
                
                # If numbered format not found, fallback to all non-empty lines
                if not lines:
                    lines = [f"{i+1}. {line.strip()}" for i, line in enumerate(text_response.split("\n")) 
                            if line.strip() and not any(skip in line.lower() for skip in ["here are", "paraphrased"])]
                
                # Add header and return
                result_lines = lines[:num_return_sequences]
                if result_lines:
                    return ["Here are three unique paraphrased versions of the text:"] + result_lines
                return result_lines
            else:
                return [f"❌ API Error {response.status_code}: {response.text}"]

        except Exception as e:
            return [f"❌ Error: {str(e)}"]