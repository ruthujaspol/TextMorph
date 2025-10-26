import re
import yake
from transformers import pipeline

class TextEnhancer:
    def __init__(self):
        # Style adaptation model (small + fast)
        self.style_model = pipeline("text2text-generation", model="t5-small", device=-1)

    # ---------- STYLE ADAPTATION ----------
    def adapt_style(self, text, tone="formal"):
        tone_prompt = {
            "formal": "Rephrase this text in a formal and professional tone: ",
            "casual": "Rephrase this text in a casual, friendly tone: ",
            "technical": "Rephrase this text using technical terminology: "
        }.get(tone.lower(), "Rephrase this text professionally: ")

        result = self.style_model(f"{tone_prompt}{text}", max_length=300)[0]['generated_text']
        return result.strip()

    # ---------- MULTI-DOCUMENT SUMMARIZATION ----------
    def merge_and_summarize(self, summarizer, docs):
        combined_text = "\n".join(docs)
        result = summarizer.abstractive_summary(combined_text, length="long")
        return result.strip()

    # ---------- KEYWORD EXTRACTION ----------
    def extract_keywords(self, text, top_k=10):
        kw_extractor = yake.KeywordExtractor(top=top_k, stopwords=None)
        keywords = kw_extractor.extract_keywords(text)
        return [word for word, score in keywords if re.match(r'^[A-Za-z]', word)]
