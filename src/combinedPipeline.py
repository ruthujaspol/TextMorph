from ExtractiveSummarizer import ExtractiveSummarizer
from AbstractiveSummarizer import AbstractiveSummarizer
from paraphraser import Paraphraser

class SummarizationPipeline:
    """Combined pipeline for Summarization (HF) + Paraphrasing (GROQ LLM)."""

    def __init__(self, hf_api_key):
        print("🔧 Initializing SummarizationPipeline...")

        # --- Extractive Summarizer ---
        try:
            self.extractive = ExtractiveSummarizer(hf_api_key)
            print("✅ Extractive Summarizer loaded")
        except Exception as e:
            print(f"⚠️ Warning: Extractive Summarizer failed: {e}")
            self.extractive = None

        # --- Abstractive Summarizer ---
        try:
            self.abstractive = AbstractiveSummarizer(hf_api_key)
            print("✅ Abstractive Summarizer loaded")
        except Exception as e:
            print(f"⚠️ Warning: Abstractive Summarizer failed: {e}")
            self.abstractive = None

        # --- GROQ Paraphraser ---
        try:
            self.paraphraser = Paraphraser()
            print("✅ GROQ Paraphraser loaded")
        except Exception as e:
            print(f"⚠️ Warning: GROQ Paraphraser failed: {e}")
            self.paraphraser = None

        print("✨ SummarizationPipeline initialized successfully!\n")

    # -------- Summarization --------
    def summarize(self, text, method="abstractive", length="medium"):
        if not text or not text.strip():
            return "⚠️ No text provided."

        # ✅ Length control logic added here
        if length.lower() == "short":
            max_len = 80
        elif length.lower() == "medium":
            max_len = 150
        else:
            max_len = 300

        try:
            if method == "extractive":
                if self.extractive is None:
                    return "❌ Extractive Summarizer unavailable."
                return self.extractive.summarize(text, length)
            else:
                if self.abstractive is None:
                    return "❌ Abstractive Summarizer unavailable."
                # ✅ Pass length control to abstractive model
                return self.abstractive.summarize(text, max_len=max_len)
        except Exception as e:
            return f"❌ Error: {e}"

    # -------- Paraphrasing --------
    def paraphrase(self, text, num_return_sequences=3):
        if self.paraphraser is None:
            return "❌ Paraphraser unavailable."
        try:
            results = self.paraphraser.paraphrase(text, num_return_sequences)
            return "\n\n".join(results)
        except Exception as e:
            return f"❌ Error in paraphrasing: {e}"

    # -------- Utilities --------
    def get_status(self):
        return {
            "extractive": self.extractive is not None,
            "abstractive": self.abstractive is not None,
            "groq_paraphraser": self.paraphraser is not None,
        }
