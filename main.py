import os
import json
import time
import pdfplumber
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

MODEL_PATH = "local_model"
PDF_FOLDER = "pdfs"
INPUT_FILE = "input.json"
OUTPUT_FILE = "output.json"

def load_input_data():
    with open(INPUT_FILE, "r") as f:
        return json.load(f)

def load_documents(input_data):
    chunks = []
    for doc in input_data["documents"]:
        file_path = os.path.join(PDF_FOLDER, doc["filename"])
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text and len(text.strip()) > 20:
                    chunks.append({
                        "document": doc["filename"],
                        "page_number": page_num,
                        "text": text.strip()
                    })
    return chunks

def embed_chunks(chunks, query, model):
    query_vec = model.encode([query])
    doc_vecs = model.encode([chunk["text"] for chunk in chunks])
    similarities = cosine_similarity(query_vec, doc_vecs)[0]

    ranked = sorted(
        zip(chunks, similarities),
        key=lambda x: x[1],
        reverse=True
    )
    return ranked[:5]

def main():
    start = time.time()
    input_data = load_input_data()

    persona = input_data["persona"]["role"]
    job = input_data["job_to_be_done"]["task"]
    query = persona + " " + job

    model = SentenceTransformer(MODEL_PATH)

    chunks = load_documents(input_data)
    top_chunks = embed_chunks(chunks, query, model)

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

    metadata = {
        "input_documents": [doc["filename"] for doc in input_data["documents"]],
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": timestamp
    }

    extracted_sections = []
    subsection_analysis = []

    for i, (chunk, _) in enumerate(top_chunks, 1):
        extracted_sections.append({
            "document": chunk["document"],
            "section_title": chunk["text"][:60].strip().replace("\n", " ") + "...",
            "importance_rank": i,
            "page_number": chunk["page_number"]
        })
        subsection_analysis.append({
            "document": chunk["document"],
            "refined_text": chunk["text"],
            "page_number": chunk["page_number"]
        })

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[✓] Completed in {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    main()
