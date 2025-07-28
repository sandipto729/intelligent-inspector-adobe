# Docker Build and Run Instructions

## Building the Docker Image

Build the Docker image using the following command:

```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

## Running the Container

Run the solution using the following command:

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
```

## Expected Behavior

The container will:

1. **Process all PDFs** from the `/app/input` directory
2. **Generate individual JSON files** in `/app/output` for each PDF (e.g., `document.pdf` → `document.json`)
3. **Create a summary file** `output.json` with processing statistics
4. **Work completely offline** with no network dependencies
5. **Use the local model** (under 200MB) for embeddings

## Input Structure

Your input directory should contain:
- PDF files to process
- (Optional) `input.json` with persona and task information

If `input.json` is present, it should follow this structure:
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

## Output Structure

For each `filename.pdf`, the container creates `filename.json` with:
- Document metadata
- Top 5 relevant text sections ranked by hybrid similarity
- Detailed subsection analysis

Plus a summary `output.json` file with processing statistics.

## Architecture

- **Platform**: linux/amd64 (AMD64 compatible)
- **No GPU dependencies**: CPU-only processing
- **Model size**: Local sentence transformer model < 200MB
- **Offline operation**: No internet connectivity required
