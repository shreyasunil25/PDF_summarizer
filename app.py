import streamlit as st
from transformers import pipeline
import torch
import pypdf
from utils import extract_text_from_pdf

st.set_page_config(page_title="Big Doc Summarizer")
st.title("📚 Long PDF Summarizer (Pegasus)")
st.markdown("Use our free summarizer")

@st.cache_resource
def load_summarizer():
    device=0 if torch.cuda.is_available() else -1
    print(f"Loading Pegasus Model on {'GPU' if device == 0 else 'CPU'}...")

    summarizer=pipeline(
        "summarization",
        model="google/pegasus-xsum",
        device=device
    )
    return summarizer

with st.spinner("Loading Pegasus model...this might take a minute on the first run."):
    summarizer_model=load_summarizer()

def chunk_text(text, max_words=400):
    words = text.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            
    # Add the last leftover chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    return chunks  # <--- THIS MUST BE ALIGNED WITH 'def', NOT INSIDE ANY IF/FOR LOOP

uploaded_file= st.file_uploader("Upload a long PDF", type="pdf")

if uploaded_file is not None:
    if st.button("Summarize Document"):
        with st.status("Processig=g=ng PDF...", expanded=True) as status:
            st.write("Extracting text from PDF...")
            raw_text=extract_text_from_pdf(uploaded_file)
            word_count=len(raw_text.split())
            st.write(f"Found {word_count} words.")

            st.write("Splitting text into manageable chunks...")
            text_chunks=chunk_text(raw_text)
            st.write(f"Split into {len(text_chunks)} parts. ")

            final_summary=[]
            progress_bar=st.progress(0)

            for i, chunk in enumerate(text_chunks):
                st.write(f"Summarizing part {i+1}/{len(text_chunks)}...")

                summary=summarizer_model(
                    chunk,
                    max_length=120,
                    min_length=60,
                    do_sample=False,
                    truncation=True
                )
                final_summary.append(summary[0]['summary_text'])

                progress_bar.progress((i+1)/len(text_chunks))

            status.update(label="Summarization Complete!", state="complete", expanded=False)
        
        st.subheader("Final Summary")
        full_summary_text=" ".join(final_summary)
        st.write(full_summary_text)

        st.download_button(
            label="Download Summary as TXT",
            data=full_summary_text,
            file_name="summary.txt",
            mime="text/plain"
        )