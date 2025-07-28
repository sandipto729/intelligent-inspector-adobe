#!/bin/bash

# Docker Build Script for Intelligent Inspector Adobe
# This script builds the Docker image locally

set -e  # Exit on any error

echo "🐳 Building Docker image for Intelligent Inspector Adobe..."
echo "📋 Build details:"
echo "   - Platform: linux/amd64"
echo "   - Image name: intelligent-inspector-adobe"
echo "   - Tag: latest"
echo ""

# Build the Docker image
docker build --platform linux/amd64 -t intelligent-inspector-adobe:latest .

echo ""
echo "✅ Docker image built successfully!"
echo "📦 Image name: intelligent-inspector-adobe:latest"
echo ""
echo "🚀 To run the container, use:"
echo "   ./docker-run.sh"
echo ""
echo "🔍 To inspect the image, use:"
echo "   docker images | grep intelligent-inspector-adobe"
