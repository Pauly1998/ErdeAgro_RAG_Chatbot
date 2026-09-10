import fitz

print("Script started...")

pdf_path = "data/erde_agro_info_03.pdf"

doc = fitz.open(pdf_path)

print("PDF opened successfully!")
print("Number of pages:", len(doc))

text = ""

for page in doc:
    text += page.get_text()

doc.close()

print("\nPDF text extracted successfully!")
print("-----------------------------------")
print(text[:3000])