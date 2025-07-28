#!/bin/bash

# Setup Script for Intelligent Inspector Adobe
# This script sets up the complete environment for testing

set -e  # Exit on any error

echo "🚀 Setting up Intelligent Inspector Adobe Docker Environment"
echo "=========================================================="
echo ""

# Create necessary directories
echo "📂 Creating directories..."
mkdir -p input output test-data

# Copy sample PDFs to input directory for testing (if they exist)
if [ -d "pdfs" ] && [ "$(ls -A pdfs)" ]; then
    echo "📋 Copying sample PDFs to input directory..."
    cp pdfs/*.pdf input/ 2>/dev/null || echo "⚠️  No PDFs found in pdfs directory"
fi

# Copy sample input.json if it exists
if [ -f "input.json" ]; then
    echo "📝 Copying input.json to input directory..."
    cp input.json input/
fi

echo ""
echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "   1. Add your PDF files to the 'input' directory"
echo "   2. (Optional) Add input.json to the 'input' directory with persona/task info"
echo "   3. Build the Docker image: ./docker-build.sh"
echo "   4. Run the container: ./docker-run.sh"
echo ""
echo "📁 Directory structure:"
echo "   input/    - Place your PDF files here"
echo "   output/   - Results will be generated here"
echo ""
