#!/bin/bash

# Docker Run Script for Intelligent Inspector Adobe
# This script runs the Docker container with proper volume mounts

set -e  # Exit on any error

echo "🐳 Running Intelligent Inspector Adobe Docker container..."
echo ""

# Check if Docker image exists
if ! docker images | grep -q "intelligent-inspector-adobe"; then
    echo "❌ Docker image 'intelligent-inspector-adobe:latest' not found!"
    echo "🔧 Please build the image first using: ./docker-build.sh"
    exit 1
fi

# Create input and output directories if they don't exist
mkdir -p input output

echo "📂 Directory setup:"
echo "   - Input directory: $(pwd)/input"
echo "   - Output directory: $(pwd)/output"
echo ""

# Check if input directory has PDF files
pdf_count=$(find input -name "*.pdf" -type f 2>/dev/null | wc -l)
if [ "$pdf_count" -eq 0 ]; then
    echo "⚠️  Warning: No PDF files found in the input directory!"
    echo "📋 Please add PDF files to the 'input' directory before running."
    echo ""
fi

echo "🚀 Starting container..."
echo "🔒 Network: Disabled (offline mode)"
echo "📊 Processing $pdf_count PDF file(s)..."
echo ""

# Run the Docker container
docker run --rm \
    -v "$(pwd)/input:/app/input" \
    -v "$(pwd)/output:/app/output" \
    --network none \
    intelligent-inspector-adobe:latest

echo ""
echo "✅ Container execution completed!"
echo "📁 Check the 'output' directory for results"
