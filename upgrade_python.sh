#!/bin/bash
# Python Upgrade Script for macOS

echo "=========================================="
echo "Python Upgrade Script"
echo "=========================================="
echo ""

# Check current Python version
CURRENT_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Current Python version: $CURRENT_VERSION"
echo ""

# Method 1: Using pyenv (Recommended - allows multiple versions)
if command -v pyenv &> /dev/null; then
    echo "✅ pyenv detected"
    echo ""
    echo "Installing Python 3.11.9 using pyenv..."
    echo "This may take a few minutes..."
    pyenv install 3.11.9
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "Setting Python 3.11.9 as local version for this project..."
        pyenv local 3.11.9
        
        echo ""
        echo "✅ Python upgraded successfully!"
        echo "New version: $(python3 --version)"
        echo ""
        echo "Now run: ./setup.sh"
        exit 0
    else
        echo "❌ pyenv installation failed. Trying Homebrew..."
    fi
fi

# Method 2: Using Homebrew
if command -v brew &> /dev/null; then
    echo "✅ Homebrew detected"
    echo ""
    echo "Installing Python 3.11 using Homebrew..."
    brew install python@3.11
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Python 3.11 installed via Homebrew"
        echo ""
        echo "To use Python 3.11, you can:"
        echo "1. Use the full path: /opt/homebrew/bin/python3.11"
        echo "2. Or create an alias in your shell config"
        echo ""
        echo "For this project, update setup.sh to use: python3.11"
        exit 0
    else
        echo "❌ Homebrew installation failed."
    fi
fi

echo ""
echo "❌ Could not install Python automatically."
echo ""
echo "Manual installation options:"
echo "1. Download from https://www.python.org/downloads/"
echo "2. Or run: brew install python@3.11"
echo "3. Or run: pyenv install 3.11.9"
