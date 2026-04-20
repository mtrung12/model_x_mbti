import numpy as np
from sentence_transformers import SentenceTransformer

model = ""
BATCH = 100

def get_embedding(text: str | list[str]):
    result = model.encode(text, show_progress_bar = False)
    if isinstance(text, list):
        return result.tolist()
    return result