from transformers import pipeline

class SummarizationPipeline:
    def __init__(self):
        # Faster model for speed
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def summarize(self, text, max_words=60):
        # Convert approximate words → tokens
        max_length = int(max_words * 1.3)
        min_length = int(max_words * 0.6)
        result = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return result[0]["summary_text"]
