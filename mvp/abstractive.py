from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class AbstractiveSummarizer:
    def __init__(self, api_key=None):
        # You don’t need api_key for local models now
        # Summarization model
        self.summarize_model_name = "facebook/bart-large-cnn"
        self.summarize_tokenizer = AutoTokenizer.from_pretrained(self.summarize_model_name)
        self.summarize_model = AutoModelForSeq2SeqLM.from_pretrained(self.summarize_model_name)

        # Paraphrasing model
        self.paraphrase_model_name = "Vamsi/T5_Paraphrase_Paws"
        self.paraphrase_tokenizer = AutoTokenizer.from_pretrained(self.paraphrase_model_name)
        self.paraphrase_model = AutoModelForSeq2SeqLM.from_pretrained(self.paraphrase_model_name)

    def summarize(self, text, length='medium'):
        length_map = {
            'short': 60,
            'medium': 130,
            'long': 200
        }
        inputs = self.summarize_tokenizer(text, return_tensors="pt", truncation=True)
        summary_ids = self.summarize_model.generate(
            **inputs,
            max_length=length_map.get(length, 130),
            min_length=30,
            early_stopping=True
        )
        return self.summarize_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    def paraphrase(self, text):
        # Add prefix as T5 expects
        input_text = "paraphrase: " + text
        inputs = self.paraphrase_tokenizer.encode(input_text, return_tensors="pt", max_length=256, truncation=True)
        outputs = self.paraphrase_model.generate(
            inputs,
            max_length=256,
            num_beams=5,
            num_return_sequences=1,
            temperature=1.5
        )
        return self.paraphrase_tokenizer.decode(outputs[0], skip_special_tokens=True)
