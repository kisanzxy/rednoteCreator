#!/bin/bash
# Make Python 3.11 the default python3 command system-wide

echo "Making Python 3.11 the default python3..."
echo ""

# Check if python3.11 exists
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Error: python3.11 not found"
    exit 1
fi

ZSH_CONFIG="$HOME/.zshrc"

# Check if alias already exists
if grep -q "alias python3='python3.11'" "$ZSH_CONFIG" 2>/dev/null; then
    echo "✅ Alias already exists in $ZSH_CONFIG"
else
    echo "" >> "$ZSH_CONFIG"
    echo "# Python 3.11 as default python3" >> "$ZSH_CONFIG"
    echo "alias python3='python3.11'" >> "$ZSH_CONFIG"
    echo "alias python='python3.11'" >> "$ZSH_CONFIG"
    echo "✅ Added aliases to $ZSH_CONFIG"
fi

echo ""
echo "To apply changes, run:"
echo "  source ~/.zshrc"
echo ""
echo "Or open a new terminal window."
echo ""
echo "Verify with: python3 --version"
