import streamlit as st
import re, time
from summarizer import SummarizationPipeline
from io import StringIO
from PyPDF2 import PdfReader
import docx
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# ---------- CONFIG ----------
st.cache_data.clear()
st.set_page_config(page_title="TextMorph", page_icon="📑", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.block-container {padding-top: 1rem; padding-bottom: 1rem;}
h1,h2,h3,h4 {color:#1E1E1E;font-family:'Poppins',sans-serif;}
.stButton>button {
    border-radius:10px;height:3rem;font-size:1.1rem;
    background:linear-gradient(90deg,#6a11cb,#2575fc);
    color:white;border:none;
}
.stButton>button:hover{opacity:0.9;}
textarea{border-radius:10px !important;}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 style='text-align:center;'>📑 TextMorph</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart Summarizer & Paraphraser with Metrics and GPU Optimization</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------- LOAD MODEL ----------
@st.cache_resource(show_spinner=True)
def load_pipeline(fast=True):
    return SummarizationPipeline(fast_mode=fast)

fast_mode = st.toggle("⚡ Fast Mode (Distil Models for Speed)", value=True)
pipeline = load_pipeline(fast=fast_mode)

# ---------- MODE SELECTION ----------
col1, col2 = st.columns(2)
with col1:
    mode = st.radio("Select Mode:", ["Summarize", "Paraphrase"], horizontal=True)
with col2:
    if mode == "Summarize":
        sum_type = st.radio("Summarization Type:", ["Abstractive", "Extractive"], horizontal=True)
        length = st.selectbox("Summary Length:", ["Short", "Medium", "Long"])
    else:
        style = st.selectbox("Paraphrasing Style:", ["Standard", "Creative", "Conservative"])

# ---------- INPUT SECTION ----------
col_in, col_out = st.columns(2)
with col_in:
    # --- INPUT TEXT FIRST ---
    st.subheader("📝 Input Text")
    input_text = st.text_area("Enter or paste text:", height=300)

    # --- FILE UPLOAD BELOW INPUT ---
    st.markdown("### 📁 Upload Files (.txt, .pdf, .docx)")
    uploaded_files = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        type=['txt', 'pdf', 'docx']
    )

    def extract_text_from_file(uploaded_file):
        if uploaded_file.name.endswith('.txt'):
            return uploaded_file.read().decode('utf-8')
        elif uploaded_file.name.endswith('.pdf'):
            pdf = PdfReader(uploaded_file)
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
        elif uploaded_file.name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            return "\n".join(p.text for p in doc.paragraphs)
        return ""

    if uploaded_files:
        combined_text = ""
        for f in uploaded_files:
            combined_text += f"\n--- {f.name} ---\n" + extract_text_from_file(f)
        if combined_text.strip():
            st.success(f"✅ Loaded {len(uploaded_files)} file(s)")
            input_text = combined_text

    run_btn = st.button(f"🚀 Run {mode}", use_container_width=True)

with col_out:
    st.subheader("🗂 Output & Stats")

    if run_btn and input_text.strip():
        start = time.time()
        with st.spinner(f"Generating {mode.lower()}..."):
            if mode == "Summarize":
                # ---- FIXED EXTRACTIVE LOGIC ----
                if sum_type == "Extractive":
                    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))
                    summarizer = LexRankSummarizer()
                    sentence_count = max(1, int(len(parser.document.sentences) * 0.3))
                    summary_sentences = summarizer(parser.document, sentence_count)
                    result = " ".join(str(s) for s in summary_sentences)
                else:
                    result = pipeline.abstractive_summary(input_text, length)
            else:
                result = pipeline.paraphrase(input_text, style)

        elapsed = time.time() - start
        st.success(f"✅ Completed in {elapsed:.2f}s")

        # ---------- DISPLAY ----------
        st.text_area(f"{mode} Result", result, height=250, key="output_area")

        # ---------- METRICS ----------
        def wc(txt): return len(re.findall(r'\w+', txt))
        in_w, out_w = wc(input_text), wc(result)
        reduction = 0 if in_w == 0 else 100 * (1 - out_w / in_w)
        colm = st.columns(3)
        colm[0].metric("Input Words", in_w)
        colm[1].metric("Output Words", out_w)
        colm[2].metric("Reduction (%)", f"{reduction:.1f}")

        # ---------- SIMILARITY ----------
        if mode == "Paraphrase":
            sim = pipeline.get_similarity(input_text, result)
            tone = pipeline.detect_tone(result)
            colm = st.columns(2)
            colm[0].metric("Semantic Similarity (%)", f"{sim:.2f}")
            colm[1].metric("Detected Tone", tone)

        # ---------- DOWNLOAD ----------
        st.download_button(
            "⬇️ Download Result",
            data=result,
            file_name=f"{mode.lower()}_output.txt",
            mime="text/plain"
        )

    elif not input_text.strip():
        st.info("👈 Enter text or upload files and click Run to start.")

st.markdown("---")
st.markdown("<div style='text-align:center; color:gray;'>Built with Streamlit • Optimized for Speed • Powered by Hugging Face</div>", unsafe_allow_html=True)
