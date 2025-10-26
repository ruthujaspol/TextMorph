import evaluate
from sentence_transformers import SentenceTransformer, util
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import re, time

rouge = evaluate.load("rouge")
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_metrics(reference, generated):
    """Compute ROUGE, BLEU, and semantic similarity between reference and generated text."""
    start = time.time()

    reference = reference.strip()
    generated = generated.strip()

    # ROUGE
    rouge_score = rouge.compute(predictions=[generated], references=[reference])
    rouge_l = round(rouge_score["rougeL"] * 100, 2)

    # BLEU
    ref_tokens = [re.findall(r'\w+', reference.lower())]
    gen_tokens = re.findall(r'\w+', generated.lower())
    smoothie = SmoothingFunction().method4
    bleu_score = round(sentence_bleu(ref_tokens, gen_tokens, smoothing_function=smoothie) * 100, 2)

    # Semantic Similarity
    emb_ref = model.encode(reference, convert_to_tensor=True)
    emb_gen = model.encode(generated, convert_to_tensor=True)
    similarity = round(util.cos_sim(emb_ref, emb_gen).item() * 100, 2)

    elapsed = round(time.time() - start, 2)
    return {
        "ROUGE-L (%)": rouge_l,
        "BLEU (%)": bleu_score,
        "Semantic Similarity (%)": similarity,
        "Evaluation Time (s)": elapsed
    }
