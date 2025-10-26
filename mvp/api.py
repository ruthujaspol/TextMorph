from flask import Flask, request, jsonify
from summarizer import SummarizationPipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize once
pipeline = SummarizationPipeline()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to TextMorph API 🚀"})

# ---------- Summarization ----------
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    mode = data.get("mode", "abstractive").lower()
    length = data.get("length", "medium").lower()

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    try:
        if mode == "extractive":
            summary = pipeline.extractive_summary(text)
        else:
            summary = pipeline.abstractive_summary(text, length)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- Paraphrasing ----------
@app.route("/paraphrase", methods=["POST"])
def paraphrase():
    data = request.get_json()
    text = data.get("text", "")
    style = data.get("style", "standard").lower()

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    try:
        paraphrased = pipeline.paraphrase(text, style)
        return jsonify({"paraphrased": paraphrased})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
