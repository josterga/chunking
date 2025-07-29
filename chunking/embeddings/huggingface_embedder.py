import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import torch

load_dotenv()
HF_MODEL = os.getenv("HF_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

tokenizer_hf = AutoTokenizer.from_pretrained(HF_MODEL)
model_hf = AutoModel.from_pretrained(HF_MODEL)

def hf_tokenizer(text):
    return tokenizer_hf.encode(text)

def huggingface_embed_fn(texts):
    inputs = tokenizer_hf(texts, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        model_output = model_hf(**inputs)
    embeddings = model_output.last_hidden_state.mean(dim=1).tolist()
    return embeddings