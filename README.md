# 🕵️ Intelligent Inspector — Document Analyzer

This project implements an **Intelligent Inspector** that extracts and ranks relevant content from a collection of PDF documents based on a defined **persona** and a specific **job-to-be-done**.  

It is designed to run entirely **offline**, on **CPU**, with a **model size ≤ 1GB**, and **< 60s** processing time for 3–5 PDFs.

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