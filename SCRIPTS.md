# Executable Docker Scripts

This directory contains executable scripts to build, run, and test the Intelligent Inspector Adobe Docker application.

## 🚀 Available Scripts

### `./setup.sh`
- Creates necessary directories (`input/`, `output/`)
- Copies sample files if available
- Prepares the environment for Docker operations

### `./docker-build.sh`
- Builds the Docker image with AMD64 platform support
- Tags the image as `intelligent-inspector-adobe:latest`
- Provides build status and next steps

### `./docker-run.sh`
- Runs the Docker container with proper volume mounts
- Maps `./input` to `/app/input` and `./output` to `/app/output`
- Runs in offline mode (`--network none`)
- Checks for PDF files before execution

### `./test.sh`
- Complete end-to-end test script
- Runs setup, build, and execution
- Validates output generation
- Provides detailed test results

## 📋 Usage Order

1. **First time setup:**
   ```bash
   ./setup.sh
   # Add your PDF files to input/
   ```

2. **Build the Docker image:**
   ```bash
   ./docker-build.sh
   ```

3. **Run the analysis:**
   ```bash
   ./docker-run.sh
   ```

4. **Run complete test (optional):**
   ```bash
   ./test.sh
   ```

## 🔧 Script Features

- **Error handling**: All scripts use `set -e` to exit on errors
- **User feedback**: Clear progress messages and status updates
- **Validation**: Check for prerequisites and required files
- **Cross-platform**: Compatible with macOS, Linux, and Windows (via WSL)

## 📁 Directory Structure After Setup

```
├── input/           # Your PDF files go here
├── output/          # Analysis results appear here
├── docker-build.sh  # Build script
├── docker-run.sh    # Run script
├── setup.sh         # Setup script
├── test.sh          # Test script
└── ...             # Other project files
```

## ⚡ Quick Commands

```bash
# Complete workflow
./setup.sh && ./docker-build.sh && ./docker-run.sh

# Run test suite
./test.sh

# Rebuild and run
./docker-build.sh && ./docker-run.sh
```
