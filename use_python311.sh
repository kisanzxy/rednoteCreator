#!/bin/bash
# Make Python 3.11 the default for this project

echo "Configuring Python 3.11 for this project..."
echo ""

# Check if python3.11 exists
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Error: python3.11 not found"
    echo "Please install Python 3.11 first: brew install python@3.11"
    exit 1
fi

# Create a local python3 symlink in the project (if possible)
# Or create a wrapper script
cat > python3_wrapper.sh << 'EOF'
#!/bin/bash
exec python3.11 "$@"
EOF

chmod +x python3_wrapper.sh

echo "✅ Created python3_wrapper.sh"
echo ""
echo "Option 1: Use python3.11 directly (recommended)"
echo "  python3.11 src/main.py"
echo ""
echo "Option 2: Add alias to your ~/.zshrc (system-wide)"
echo "  echo \"alias python3='python3.11'\" >> ~/.zshrc"
echo "  source ~/.zshrc"
echo ""
echo "Option 3: Use the wrapper (for this project)"
echo "  ./python3_wrapper.sh src/main.py"
