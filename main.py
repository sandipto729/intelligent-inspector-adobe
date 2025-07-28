import os
import json
import time
import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from rank_bm25 import BM25Okapi
import glob

MODEL_PATH = "local_model"
INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
ALPHA = 0.6  # Weight for dense score (0.6 = 60% dense + 40% BM25)

def load_input_data():
    """Load input.json from the input directory"""
    input_file = os.path.join(INPUT_DIR, "input.json")
    if os.path.exists(input_file):
        with open(input_file, "r") as f:
            return json.load(f)
    return None

def extract_text_from_pdf(pdf_path):
    """Extract text chunks from a single PDF file"""
    chunks = []
    filename = os.path.basename(pdf_path)
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text and len(text.strip()) > 20:
                    chunks.append({
                        "document": filename,
                        "page_number": page_num,
                        "text": text.strip()
                    })
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")
    
    return chunks

def hybrid_rank_chunks(chunks, query, model, alpha=0.6):
    """Rank chunks using hybrid approach (dense + BM25)"""
    if not chunks:
        return []
    
    texts = [chunk["text"] for chunk in chunks]
    
    # Dense embeddings and cosine similarity
    query_vec = model.encode([query])
    doc_vecs = model.encode(texts)
    dense_scores = cosine_similarity(query_vec, doc_vecs)[0]

    # BM25 scores
    tokenized_texts = [text.lower().split() for text in texts]
    bm25 = BM25Okapi(tokenized_texts)
    bm25_scores = bm25.get_scores(query.lower().split())

    # Normalize both scores to 0–1
    scaler = MinMaxScaler()
    dense_norm = scaler.fit_transform(np.array(dense_scores).reshape(-1, 1)).flatten()
    
    # Handle case where all BM25 scores are zero
    if np.all(bm25_scores == 0):
        bm25_norm = np.zeros_like(bm25_scores)
    else:
        bm25_norm = scaler.fit_transform(np.array(bm25_scores).reshape(-1, 1)).flatten()

    # Combine scores
    hybrid_scores = alpha * dense_norm + (1 - alpha) * bm25_norm

    # Zip with chunks and sort
    ranked = sorted(
        zip(chunks, hybrid_scores),
        key=lambda x: x[1],
        reverse=True
    )
    return ranked[:5]

def process_single_pdf(pdf_path, query, model):
    """Process a single PDF and return the analysis"""
    filename = os.path.basename(pdf_path)
    print(f"Processing {filename}...")
    
    chunks = extract_text_from_pdf(pdf_path)
    if not chunks:
        print(f"Warning: No text chunks extracted from {filename}")
        return None
    
    top_chunks = hybrid_rank_chunks(chunks, query, model, alpha=ALPHA)
    
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    
    metadata = {
        "input_document": filename,
        "query": query,
        "processing_timestamp": timestamp,
        "total_chunks": len(chunks),
        "top_chunks_selected": len(top_chunks)
    }

    extracted_sections = []
    subsection_analysis = []

    for i, (chunk, score) in enumerate(top_chunks, 1):
        extracted_sections.append({
            "document": chunk["document"],
            "section_title": chunk["text"][:60].strip().replace("\n", " ") + "...",
            "importance_rank": i,
            "page_number": chunk["page_number"],
            "relevance_score": float(score)
        })
        subsection_analysis.append({
            "document": chunk["document"],
            "refined_text": chunk["text"],
            "page_number": chunk["page_number"],
            "relevance_score": float(score)
        })

    output = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }
    
    return output

def main():
    start_time = time.time()
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load model
    print("Loading model...")
    try:
        model = SentenceTransformer(MODEL_PATH)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return
    
    # Load input data for query construction
    input_data = load_input_data()
    if input_data:
        persona = input_data.get("persona", {}).get("role", "User")
        job = input_data.get("job_to_be_done", {}).get("task", "Analyze document")
        query = f"{persona} {job}"
        print(f"Using query: {query}")
    else:
        query = "Analyze and extract relevant information"
        print(f"No input.json found, using default query: {query}")
    
    # Find all PDF files in input directory
    pdf_pattern = os.path.join(INPUT_DIR, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF file
    processed_count = 0
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        output_filename = filename.replace('.pdf', '.json')
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        try:
            result = process_single_pdf(pdf_path, query, model)
            if result:
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=2)
                print(f"✓ Created {output_filename}")
                processed_count += 1
            else:
                print(f"✗ Failed to process {filename}")
        except Exception as e:
            print(f"✗ Error processing {filename}: {str(e)}")
    
    # Create summary output.json
    summary_output = {
        "processing_summary": {
            "total_pdfs_found": len(pdf_files),
            "successfully_processed": processed_count,
            "processing_time_seconds": round(time.time() - start_time, 2),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            "query_used": query
        },
        "processed_files": [os.path.basename(f).replace('.pdf', '.json') for f in pdf_files]
    }
    
    summary_path = os.path.join(OUTPUT_DIR, "output.json")
    with open(summary_path, "w") as f:
        json.dump(summary_output, f, indent=2)
    
    print(f"\n[✓] Processing completed in {time.time() - start_time:.2f} seconds")
    print(f"[✓] Processed {processed_count}/{len(pdf_files)} PDFs")
    print(f"[✓] Output files saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
