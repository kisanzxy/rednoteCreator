#!/bin/bash
# Activate Python 3.11 for this shell session

# Add Python 3.11 to the front of PATH for this session
export PATH="/usr/local/bin:$PATH"

# Create alias for python3 to use python3.11
alias python3='python3.11'
alias python='python3.11'

echo "✅ Python 3.11 activated for this session"
echo "python3 now points to: $(python3 --version)"
echo ""
echo "To make this permanent, add to your ~/.zshrc:"
echo "  alias python3='python3.11'"
echo "  alias python='python3.11'"
