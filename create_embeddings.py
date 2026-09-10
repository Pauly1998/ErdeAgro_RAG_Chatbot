import json
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------------
# 1. Load chunks
# -----------------------------------

with open("data/chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

texts = [chunk["text"] for chunk in chunks]

print("Total chunks:", len(texts))


# -----------------------------------
# 2. Load embedding model
# -----------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")


# -----------------------------------
# 3. Create embeddings
# -----------------------------------

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

print("Embeddings created successfully!")
print("Number of embeddings:", len(embeddings))
print("Embedding dimensions:", len(embeddings[0]))


# -----------------------------------
# 4. Save embeddings
# -----------------------------------

np.save("data/embeddings.npy", embeddings)

print("Embeddings saved successfully!")
print("File: data/embeddings.npy")