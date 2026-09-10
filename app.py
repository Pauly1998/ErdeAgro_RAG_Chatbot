from pathlib import Path
import json

import faiss
import numpy as np
import ollama
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

CHUNKS_FILE = BASE_DIR / "New folder" / "chunks.json"
INDEX_FILE = BASE_DIR / "New folder" / "erde_agro.index"


# ============================================================
# SETTINGS
# ============================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3.2:3b"
TOP_K = 3


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL,
    backend="onnx"
)


# ============================================================
# LOAD FAISS INDEX
# ============================================================

print("Loading FAISS index...")

index = faiss.read_index(str(INDEX_FILE))


# ============================================================
# LOAD CHUNKS
# ============================================================

print("Loading chunks...")

with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
    chunks = json.load(file)


print("ERDE Agro RAG loaded successfully!")
print(f"Total chunks: {len(chunks)}")


# ============================================================
# GET CHUNK TEXT
# ============================================================

def get_chunk_text(chunk):

    if isinstance(chunk, dict):
        return chunk.get("text") or chunk.get("content") or ""

    return str(chunk)


# ============================================================
# RETRIEVE RELEVANT INFORMATION
# ============================================================

def retrieve(question):

    query_embedding = embedding_model.encode(
        [question],
        convert_to_numpy=True
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    k = min(TOP_K, index.ntotal)

    distances, indices = index.search(
        query_embedding,
        k
    )

    results = []

    for idx in indices[0]:

        if 0 <= idx < len(chunks):

            text = get_chunk_text(chunks[idx])

            if text.strip():
                results.append(text)

    return results


# ============================================================
# ASK OLLAMA
# ============================================================

def ask_ollama(question, context):

    context_text = "\n\n".join(context)

    prompt = f"""
You are ERDE Agro AI Assistant.

Use the following ERDE Agro knowledge base to answer the user's question.

KNOWLEDGE BASE:
{context_text}

USER QUESTION:
{question}

RULES:

1. Use the knowledge base as the primary source.
2. Do not invent ERDE Agro information.
3. Do not make up products, crops, services, certifications,
   locations, or contact details.
4. If the answer is not available in the knowledge base, say:

"I don't have that information in my knowledge base."

5. Give a clear and useful answer.
6. Use bullet points when appropriate.
7. Be professional and friendly.
8. Do not mention RAG, FAISS, embeddings, or internal
   implementation unless the user specifically asks.
"""

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template("index.html")


# ============================================================
# CHAT API
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:

        return jsonify({
            "answer": "Please enter a question."
        })

    try:

        relevant_chunks = retrieve(question)

        if not relevant_chunks:

            return jsonify({
                "answer": "I don't have that information in my knowledge base."
            })

        answer = ask_ollama(
            question,
            relevant_chunks
        )

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        print("ERROR:", e)

        return jsonify({
            "answer": "Sorry, something went wrong. Please try again."
        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        debug=False,
        host="0.0.0.0",
        port=port
    )