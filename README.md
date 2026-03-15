# Long PDF Summarizer 📚

Upload any long PDF document and get a structured summary — runs entirely 
locally using Google's Pegasus transformer model, no API key needed.

## What Makes This Different
Most PDF summarizers send your document to an external API. This one runs 
the Pegasus-XSum model locally — your data never leaves your machine.

## Features
- Handles long documents by chunking text into 400-word segments
- Summarizes each chunk with Pegasus-XSum (state-of-the-art abstractive summarization)
- Progress bar showing summarization status per chunk
- Download final summary as .txt
- GPU acceleration if available, falls back to CPU automatically

## Tech Stack
- Python, Streamlit
- HuggingFace Transformers (google/pegasus-xsum)
- PyTorch
- pypdf

## Setup

pip install -r requirements.txt
streamlit run app.py

Note: First run downloads the Pegasus model (~2GB). Requires ~4GB RAM.
GPU recommended for large documents but not required.

## How It Works
Text is extracted from the PDF, split into 400-word chunks to fit the 
model's context window, each chunk is summarized independently by Pegasus, 
and the summaries are concatenated into a final output.
