#!/bin/bash
# Build script to package the IPA

# Create executable if it doesn't exist
if [ ! -f "Payload/Fearn.app/Fearn" ]; then
    echo "Creating placeholder executable..."
    touch "Payload/Fearn.app/Fearn"
    chmod +x "Payload/Fearn.app/Fearn"
fi

# Run the IPA builder
python3 fearn_ipa_builder.py \
    --name "Fearn" \
    --bundle-id "com.krnlthemodder.fearn" \
    --version "1.0" \
    --output "." \
    --verbose
