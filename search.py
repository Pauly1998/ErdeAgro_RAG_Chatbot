import os
import json
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from groq import Groq


# ============================================================
# 1. LOAD ERDE AGRO CHUNKS
# ============================================================

print("Loading ERDE Agro data...")

with open(
    "New folder/chunks.json",
    "r",
    encoding="utf-8"
) as file:
    chunks = json.load(file)

print(f"Chunks loaded: {len(chunks)}")


# ============================================================
# 2. LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded!")


# ============================================================
# 3. LOAD FAISS INDEX
# ============================================================

print("\nLoading FAISS index...")

index = faiss.read_index(
    "New folder/erde_agro.index"
)

print("FAISS index loaded!")
print(f"Total vectors: {index.ntotal}")


# ============================================================
# 4. CONNECT TO GROQ
# ============================================================

print("\nConnecting to Groq...")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY not found.")
    print("Please set your Groq API key first.")
    exit()

client = Groq(
    api_key=api_key
)

print("Groq connected successfully!")


# ============================================================
# 5. CHATBOT LOOP
# ============================================================

print("\n" + "=" * 60)
print("              ERDE AGRO AI ASSISTANT")
print("=" * 60)

print("\nYou can ask multiple questions.")
print("Type 'exit' to stop the chatbot.")


while True:

    # ========================================================
    # ASK USER QUESTION
    # ========================================================

    query = input("\nYou: ")

    if query.lower() == "exit":
        print("\nGoodbye! 👋")
        break


    # ========================================================
    # CREATE QUESTION EMBEDDING
    # ========================================================

    print("\nSearching ERDE Agro information...")

    query_embedding = embedding_model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )


    # ========================================================
    # SEARCH FAISS
    # ========================================================

    k = 3

    distances, indices = index.search(
        query_embedding,
        k
    )


    # ========================================================
    # COLLECT RELEVANT CHUNKS
    # ========================================================

    context = ""

    for index_number in indices[0]:

        context += chunks[index_number]["text"]
        context += "\n\n"


    # ========================================================
    # SHOW RETRIEVED INFORMATION
    # ========================================================

    print("\nRelevant information retrieved from ERDE Agro data.")


    # ========================================================
    # CREATE PROMPT
    # ========================================================

    prompt = f"""
You are an AI assistant for ERDE Agro.

Answer the user's question using ONLY the information
provided in the context below.

Do not make up information.

If the answer is not available in the context, say:

"I don't have that information in the ERDE Agro data."

Give a clear, simple and helpful answer.

CONTEXT:
{context}

USER QUESTION:
{query}
"""


    # ========================================================
    # SEND REQUEST TO GROQ
    # ========================================================

    print("Sending information to Groq...")


    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )


    print("Groq response received!")


    # ========================================================
    # GET ANSWER
    # ========================================================

    answer = response.choices[0].message.content


    # ========================================================
    # DISPLAY ANSWER
    # ========================================================

    print("\nERDE Agro Assistant:")
    print("-----------------------------------")
    print(answer)
    print("-----------------------------------")