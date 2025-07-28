# 🕵️ Intelligent Inspector — Document Analyzer (Docker Edition)

A dockerized PDF document analysis tool that uses hybrid ranking (dense embeddings + BM25) to extract and analyze relevant sections from PDF documents based on a defined **persona** and a specific **job-to-be-done**.

It is designed to run entirely **offline**, on **CPU**, with a **model size ≤ 200MB**, and works with Docker containers for easy deployment.

---

## 🚀 Quick Start

### Prerequisites
- Docker installed and running
- PDF files to analyze

### Setup and Run

1. **Initial Setup**
   ```bash
   ./setup.sh
   ```

2. **Add your PDF files to the input directory**
   ```bash
   cp your-pdfs/*.pdf input/
   ```

3. **Build the Docker image**
   ```bash
   ./docker-build.sh
   ```

4. **Run the analysis**
   ```bash
   ./docker-run.sh
   ```

5. **Check results in the output directory**
   ```bash
   ls output/
   ```

## 📁 Directory Structure

```
├── input/           # Place your PDF files here
├── output/          # Analysis results will appear here
├── local_model/     # Pre-trained sentence transformer model (88MB)
├── main.py          # Main application code
├── Dockerfile       # Docker configuration
├── docker-build.sh  # Build script
├── docker-run.sh    # Run script
├── setup.sh         # Initial setup script
└── requirements.txt # Python dependencies
```

## 🔧 Manual Docker Commands

If you prefer to run Docker commands manually:

### Build
```bash
docker build --platform linux/amd64 -t intelligent-inspector-adobe:latest .
```

### Run
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  intelligent-inspector-adobe:latest
```

## 📊 Input Format

### Required
- PDF files in the `input/` directory

### Optional
- `input.json` with persona and task information:
```json
{
  "persona": {
    "role": "Travel Planner"
  },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

## 📈 Output Format

For each `document.pdf`, the system generates:
- `document.json` - Individual analysis results
- `output.json` - Processing summary

### Sample Output Structure
```json
{
  "metadata": {
    "input_document": "sample.pdf",
    "query": "Travel Planner Plan a trip...",
    "processing_timestamp": "2025-07-28T12:00:00",
    "total_chunks": 25,
    "top_chunks_selected": 5
  },
  "extracted_sections": [
    {
      "document": "sample.pdf",
      "section_title": "Introduction to Travel Planning...",
      "importance_rank": 1,
      "page_number": 1,
      "relevance_score": 0.95
    }
  ],
  "subsection_analysis": [
    {
      "document": "sample.pdf",
      "refined_text": "Full text content...",
      "page_number": 1,
      "relevance_score": 0.95
    }
  ]
}
```

## ⚙️ Technical Specifications

- **Platform**: linux/amd64 (AMD64 compatible)
- **Architecture**: CPU-only processing (no GPU required)
- **Model Size**: 88MB (well under 200MB limit)
- **Network**: Completely offline operation
- **Processing**: Hybrid ranking using sentence transformers + BM25
- **Memory**: Optimized for efficient text processing

## 🐳 Docker Hub Deployment

To push to Docker Hub:

```bash
# Tag the image
docker tag intelligent-inspector-adobe:latest your-dockerhub-username/intelligent-inspector-adobe:latest

# Push to Docker Hub
docker push your-dockerhub-username/intelligent-inspector-adobe:latest
```

## 🔍 Troubleshooting

### No PDF files found
- Ensure PDF files are in the `input/` directory
- Check file permissions

### Docker build fails
- Ensure Docker is running
- Check available disk space (model files are 88MB)

### Container exits immediately
- Check logs: `docker logs $(docker ps -lq)`
- Verify input directory has PDF files

---

## 📁 Folder Structure

```
intelligent-inspector/
│
├── local_model/         # Folder where the model will be downloaded
├── input/               # Input PDF documents
├── output.json          # Final output (generated after processing)
├── model.py             # Downloads and prepares the model locally
├── main.py              # Main script: loads model, processes PDFs, outputs results
├── utils.py             # Utility functions (e.g., PDF parsing, section ranking)
├── requirements.txt     # All Python dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Usage

### 1. ✅ Install Dependencies

Make sure you're using **Python 3.8+** and have `pip` installed.

```bash
pip install -r requirements.txt
```

### 2. ⬇️ Download the Model

Run the following to download the lightweight language model (~<1GB) into `local_model/`:

```bash
python model.py
```

### 3. 🚀 Run the Inspector

Process your input PDFs and generate the output:

```bash
python main.py
```

The script will:
- Read the input JSON (persona + task)
- Analyze all PDFs inside the `input/` folder
- Extract relevant sections and refined summaries
- Write a structured `output.json` with metadata, ranked sections, and content

---

## 🔒 Constraints (Challenge Compliance)

| Constraint | Status |
|------------|--------|
| CPU-only | ✅ Supported |
| Model size ≤ 1GB | ✅ Supported |
| Execution time ≤ 60 sec | ✅ Optimized |
| No internet during run | ✅ Offline-ready |

---

## 👤 Example Persona Input

```json
{
  "persona": { "role": "Travel Planner" },
  "job_to_be_done": {
    "task": "Plan a trip of 4 days for a group of 10 college friends."
  }
}
```

PDFs in `input/` must match the document list provided in `input.json`.

---

## 📦 Output Format

The final `output.json` contains:
- **Metadata**: list of PDFs, persona, job-to-be-done, timestamp
- **Extracted Sections**: top 5 sections with page numbers and importance rank
- **Subsection Analysis**: detailed refined summaries

---

## 🐳 Optional: Run with Docker

You can build and run in an isolated Docker environment (CPU-only):

```bash
docker build -t intelligent-inspector .
docker run --rm -v $(pwd):/app intelligent-inspector
```

*(You must first copy your PDFs and input.json into the root folder before building)*

---

## 🧠 Model

The model is a small transformer-based LLM (< 1GB) for semantic similarity and ranking.  
It runs completely offline after downloading using `model.py`.

---

## 📩 Contact

**Developed by Sandipto Roy**

If you'd like to contribute or need support, feel free to raise an issue or email: sandipto729@gmail.com