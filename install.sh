#!/bin/bash
# Fearn IPA Signer - Installation and setup script

echo "Fearn IPA Signer - Setup"
echo "========================"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check for Xcode tools
if ! command -v codesign &> /dev/null; then
    echo "Error: Xcode Command Line Tools not installed"
    echo "Run: xcode-select --install"
    exit 1
fi

echo "✓ Xcode tools found"

# Make scripts executable
echo "Making scripts executable..."
chmod +x fearn.py fearn_signer.py fearn_cert_manager.py fearn_batch_signer.py fearn_validator.py

echo "✓ Scripts are executable"

# Create symbolic links (optional)
echo ""
echo "Installation complete!"
echo ""
echo "Usage:"
echo "  python3 fearn_signer.py --help"
echo "  python3 fearn_cert_manager.py --help"
echo "  python3 fearn_batch_signer.py --help"
echo "  python3 fearn_validator.py --help"
echo ""
echo "Or use the wrapper:"
echo "  python3 fearn.py fearn-signer --help"
echo ""
