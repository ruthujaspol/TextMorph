import streamlit as st
from summarizer import TextMorphPipeline

# Custom CSS
st.set_page_config(page_title="TextMorph", page_icon="🧠", layout="wide")
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-title'>TextMorph</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>AI-Powered Text Summarizer & Paraphraser</p>", unsafe_allow_html=True)

# Load pipeline once
@st.cache_resource
def load_pipeline():
    return TextMorphPipeline()

pipeline = load_pipeline()

# Mode selection
mode = st.radio("Select Task:", ["Summarize", "Paraphrase"], horizontal=True)

# Text input & layout
col1, col2 = st.columns(2)
with col1:
    st.subheader("📝 Input Text")
    text = st.text_area("Enter your text here", height=300, placeholder="Paste or type text...")

    if mode == "Summarize":
        length = st.select_slider("Select Summary Length", options=["Short", "Medium", "Long"], value="Medium")
    else:
        length = None

    if st.button("🚀 Process", use_container_width=True, type="primary"):
        if not text.strip():
            st.warning("⚠️ Please enter some text first.")
        else:
            with st.spinner("AI Processing..."):
                try:
                    if mode == "Summarize":
                        output = pipeline.summarize(text, length.lower())
                    else:
                        output = pipeline.paraphrase(text)
                    st.session_state["output"] = output
                    st.success(f"✅ {mode} Completed!")
                except Exception as e:
                    st.error(f"Error: {e}")

with col2:
    st.subheader("📘 Output")
    if "output" in st.session_state:
        st.markdown(f"<div class='output-box'>{st.session_state['output']}</div>", unsafe_allow_html=True)
    else:
        st.info("🪶 The processed output will appear here...")

# Footer
st.markdown("<hr><p style='text-align:center; color:gray;'>✨ Built with Streamlit • Powered by Hugging Face</p>", unsafe_allow_html=True)
