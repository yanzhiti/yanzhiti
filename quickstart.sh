#!/bin/bash

# Quick start script for 衍智体 (YANZHITI) Python

echo "衍智体 (YANZHITI) Python - Quick Start"
echo "================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -e ".[dev]"

echo ""
echo "Installation complete!"
echo ""
echo "To get started:"
echo "  1. Set your API key: export YANZHITI_API_KEY=your-key"
echo "  2. Run 衍智体 (YANZHITI): yanzhiti"
echo "  3. Or use the short alias: ccd"
echo ""
echo "For more information, see README.md"
