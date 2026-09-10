import numpy as np
import faiss

# -----------------------------------
# 1. Load embeddings
# -----------------------------------

embeddings = np.load("data/embeddings.npy")

print("Embeddings loaded!")
print("Shape:", embeddings.shape)


# -----------------------------------
# 2. Get embedding dimension
# -----------------------------------

dimension = embeddings.shape[1]

print("Embedding dimension:", dimension)


# -----------------------------------
# 3. Create FAISS index
# -----------------------------------

index = faiss.IndexFlatL2(dimension)

print("FAISS index created!")


# -----------------------------------
# 4. Add embeddings to index
# -----------------------------------

index.add(embeddings.astype("float32"))

print("Embeddings added to FAISS!")
print("Total vectors in index:", index.ntotal)


# -----------------------------------
# 5. Save FAISS index
# -----------------------------------

faiss.write_index(
    index,
    "data/erde_agro.index"
)

print("FAISS index saved successfully!")
print("File: data/erde_agro.index")