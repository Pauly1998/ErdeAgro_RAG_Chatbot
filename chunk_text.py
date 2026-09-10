import fitz
import json

pdf_path = "data/erde_agro_info_03.pdf"

doc = fitz.open(pdf_path)

text = ""

for page in doc:
    text += page.get_text() + "\n"

doc.close()

# Clean text
text = text.replace("\n", " ")
text = " ".join(text.split())

# Chunk settings
chunk_size = 1000
overlap = 200

chunks = []

start = 0

while start < len(text):
    end = start + chunk_size

    chunk = text[start:end]

    chunks.append({
        "chunk_id": len(chunks),
        "text": chunk
    })

    start = end - overlap

# Save chunks
with open("data/chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

print("Text extracted successfully!")
print("Total characters:", len(text))
print("Total chunks:", len(chunks))
print("Chunks saved successfully!")
print("File: data/chunks.json")