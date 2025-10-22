from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Paraphraser:
    def __init__(self):
        # Use a smaller, faster model
        model_name = "humarin/chatgpt_paraphraser_on_T5_base"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def paraphrase(self, text):
        prompt = f"paraphrase: {text}"
        inputs = self.tokenizer([prompt], return_tensors="pt", padding=True)
        outputs = self.model.generate(
            **inputs,
            max_length=256,
            num_beams=4,
            num_return_sequences=1,
            temperature=1.2,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
