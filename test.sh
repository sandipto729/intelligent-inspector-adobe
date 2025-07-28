#!/bin/bash

# Test Script for Intelligent Inspector Adobe
# This script runs a complete test of the Docker setup

set -e  # Exit on any error

echo "🧪 Testing Intelligent Inspector Adobe Docker Setup"
echo "=================================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Run setup
echo ""
echo "📋 Running setup..."
./setup.sh

# Check if we have test PDFs
if [ -d "pdfs" ] && [ "$(ls -A pdfs 2>/dev/null)" ]; then
    echo "📄 Found test PDFs, copying to input directory..."
    cp pdfs/*.pdf input/ 2>/dev/null || true
fi

# Build the image
echo ""
echo "🔨 Building Docker image..."
./docker-build.sh

# Check input directory
pdf_count=$(find input -name "*.pdf" -type f 2>/dev/null | wc -l)
if [ "$pdf_count" -eq 0 ]; then
    echo ""
    echo "⚠️  No PDF files found for testing."
    echo "📋 To run a full test, add PDF files to the input directory and run ./docker-run.sh"
    exit 0
fi

# Run the container
echo ""
echo "🚀 Running container with $pdf_count PDF file(s)..."
./docker-run.sh

# Check output
output_count=$(find output -name "*.json" -type f 2>/dev/null | wc -l)
echo ""
echo "📊 Test Results:"
echo "   - Input PDFs: $pdf_count"
echo "   - Output JSONs: $output_count"

if [ "$output_count" -gt 0 ]; then
    echo "✅ Test completed successfully!"
    echo ""
    echo "📁 Generated files:"
    ls -la output/
else
    echo "❌ Test failed - no output files generated"
    exit 1
fi
