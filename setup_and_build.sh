#!/bin/bash
# Complete setup script for building signable IPA with certificates and provisioning

set -e

echo "========================================"
echo "  Fearn Complete Build Setup"
echo "========================================"
echo ""

# Step 1: Generate certificates and provisioning profile
echo "[1/3] Generating certificates and provisioning profile..."
python3 fearn_cert_provisioning_generator.py \
    --bundle-id "com.krnlthemodder.fearn" \
    --team-id "XXXXXXXXXX" \
    --name "Fearn" \
    --verbose

echo ""
echo "[2/3] Ensuring executable exists in Payload..."

# Step 2: Ensure executable exists
if [ ! -f "Payload/Fearn.app/Fearn" ]; then
    echo "Creating placeholder executable..."
    touch "Payload/Fearn.app/Fearn"
    chmod +x "Payload/Fearn.app/Fearn"
else
    echo "Executable already exists"
fi

echo ""
echo "[3/3] Building IPA..."

# Step 3: Build the IPA
python3 fearn_ipa_builder.py \
    --name "Fearn" \
    --bundle-id "com.krnlthemodder.fearn" \
    --version "1.0" \
    --output "." \
    --verbose

echo ""
echo "========================================"
echo "  Build Complete!"
echo "========================================"
echo ""
echo "Next: Sign the IPA with:"
echo "  python3 fearn_signer.py resign -i Fearn-1.0.ipa -c 'Fearn Self-Signed' -o Fearn-signed.ipa"
echo ""
