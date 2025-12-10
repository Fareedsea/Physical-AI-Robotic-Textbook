#!/bin/bash
# Test deployment workflow in staging environment

echo "Testing deployment workflow..."

# Check if required tools are available
if ! command -v npm &> /dev/null; then
    echo "npm is required but not installed. Aborting."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "node is required but not installed. Aborting."
    exit 1
fi

echo "✓ Node.js and npm are available"

# Navigate to the website directory
cd my-website

# Install dependencies
echo "Installing dependencies..."
npm ci

if [ $? -ne 0 ]; then
    echo "Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed successfully"

# Build the website
echo "Building the website..."
npm run build

if [ $? -ne 0 ]; then
    echo "Failed to build the website"
    exit 1
fi

echo "✓ Website built successfully"

# Check if build directory exists
if [ -d "build" ]; then
    echo "✓ Build directory exists"
else
    echo "Build directory does not exist"
    exit 1
fi

# Count the number of files in build directory
file_count=$(find build -type f | wc -l)
echo "✓ Build contains $file_count files"

echo "Deployment workflow test completed successfully!"