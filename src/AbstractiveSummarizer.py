import requests
import os 

class AbstractiveSummarizer:
    """Abstractive summarization using BART model. Generates new sentences that capture the meaning of the original text."""
    
    def __init__(self, api_key): 
        self.api_key = api_key 
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn" 
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def summarize(self, text, length='medium'):
        """
        Generate abstractive summary from text.
        
        Args:
            text (str): Input text to summarize
            length (str): 'short', 'medium', or 'long'
            
        Returns:
            str: Generated summary
        """
        length_map = {
            'short': {"max_length": 60, "min_length": 30},
            'medium': {"max_length": 130, "min_length": 60},
            'long': {"max_length": 200, "min_length": 130}
        }
        
        params = length_map.get(length, length_map['medium'])
        payload = {
            "inputs": text,
            "parameters": {
                **params,
                "do_sample": True,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("summary_text", "No summary generated")
                else:
                    return str(result)
            elif response.status_code == 503:
                return "⚠️ Model is loading. Please try again in a few moments."
            else:
                return f"❌ API Error: {response.status_code} - {response.text}"
        except requests.exceptions.Timeout:
            return "❌ Request timeout. Please try again."
        except Exception as e:
            return f"❌ Error: {str(e)}"


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    HF_API_KEY = os.getenv("HF_API_KEY")

    if not HF_API_KEY:
        print("⚠️ Please set your Hugging Face API key in the environment variable 'HF_API_KEY'")
    else:
        print("\n🚀 Testing Abstractive Summarizer...\n")
        
        summarizer = AbstractiveSummarizer(HF_API_KEY)

        text = """
        Artificial Intelligence (AI) is revolutionizing industries by automating repetitive tasks,
        improving decision-making, and enhancing human creativity. From healthcare and education to
        finance and transportation, AI-driven solutions are reshaping how we live and work.
        """

        print("📄 Original Text:\n", text)
        print("\n🧠 Abstractive Summary:\n", summarizer.summarize(text))