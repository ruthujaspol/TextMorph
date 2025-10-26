from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import torch


class SummarizationPipeline:
    def __init__(self, fast_mode=True):
        # ---------- Device Setup ----------
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Using device: {self.device}")

        # ---------- Model Choice ----------
        if fast_mode:
            abs_model = "sshleifer/distilbart-cnn-12-6"
            para_model = "t5-small"
        else:
            abs_model = "facebook/bart-large-cnn"
            para_model = "ramsrigouthamg/t5_paraphraser"

        # ---------- Load Models ----------
        self.abstractive_model = pipeline(
            "summarization",
            model=abs_model,
            device=0 if self.device == "cuda" else -1
        )

        self.paraphrase_model = pipeline(
            "text2text-generation",
            model=para_model,
            device=0 if self.device == "cuda" else -1
        )

        self.tone_detector = pipeline(
            "zero-shot-classification",
            model="valhalla/distilbart-mnli-12-1",
            device=0 if self.device == "cuda" else -1
        )

        # Sentence similarity model
        self.sim_model = SentenceTransformer("all-MiniLM-L6-v2", device=self.device)

    # ---------- Extractive Summarization ----------
    def extractive_summary(self, text, sentence_count=3):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary = summarizer(parser.document, sentence_count)
        return " ".join([str(sentence) for sentence in summary])

    # ---------- Abstractive Summarization ----------
    def abstractive_summary(self, text, length="medium"):
        length = length.lower()
        min_len = 40 if length == "short" else 80 if length == "medium" else 120
        max_len = 120 if length == "short" else 200 if length == "medium" else 300
        result = self.abstractive_model(
            text, max_length=max_len, min_length=min_len, do_sample=False
        )[0]["summary_text"]
        return result.strip()

    # ---------- Paraphrasing ----------
    def paraphrase(self, text, style="standard"):
        temp = 0.9 if style.lower() == "creative" else 0.5 if style.lower() == "conservative" else 0.7
        result = self.paraphrase_model(
            f"paraphrase: {text}", max_length=200, temperature=temp
        )[0]["generated_text"]
        return result.strip()

    # ---------- Similarity ----------
    def get_similarity(self, text1, text2):
        sim = util.cos_sim(
            self.sim_model.encode(text1, convert_to_tensor=True),
            self.sim_model.encode(text2, convert_to_tensor=True),
        )
        return float(sim.item()) * 100

    # ---------- Tone Detection ----------
    def detect_tone(self, text):
        tone = self.tone_detector(
            text, candidate_labels=["informative", "analytical", "descriptive"]
        )
        return tone["labels"][0].capitalize()
