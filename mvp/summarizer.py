from transformers import pipeline

class TextMorphPipeline:
    def __init__(self):
        # Light, fast models
        self.summarizer = pipeline("summarization", model="facebook/bart-base")
        self.paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

    def summarize(self, text, length="medium"):
        min_len, max_len = {"short": (20, 60), "medium": (60, 120), "long": (120, 180)}.get(length, (60, 120))
        result = self.summarizer(text, min_length=min_len, max_length=max_len, do_sample=False)
        return result[0]["summary_text"]

    def paraphrase(self, text):
        output = self.paraphraser(f"paraphrase: {text}", max_length=256, num_return_sequences=1)
        return output[0]["generated_text"]
