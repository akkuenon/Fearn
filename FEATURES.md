# Fearn IPA Signer Features

## Overview

Fearn is a comprehensive iOS IPA file signing and management suite. It provides tools for signing, validating, managing certificates, and batch processing IPA files.

## Features

### 1. **IPA Signer** (`fearn_signer.py`)
Main tool for signing and managing individual IPA files.

**Commands:**
- `resign` - Re-sign an IPA file with a new certificate
- `extract` - Extract IPA contents
- `verify` - Verify code signature
- `info` - Display app information from Info.plist

**Usage:**
```bash
# Re-sign an IPA
python3 fearn_signer.py resign -i app.ipa -c "iPhone Developer" -o app-signed.ipa

# Verify signature
python3 fearn_signer.py verify -i app.ipa

# Extract IPA
python3 fearn_signer.py extract -i app.ipa

# Get app information
python3 fearn_signer.py info -i app.ipa
```

### 2. **Certificate Manager** (`fearn_cert_manager.py`)
Manage iOS certificates and provisioning profiles.

**Commands:**
- `list-certs` - List available signing certificates
- `list-profiles` - List provisioning profiles
- `import-cert` - Import a certificate into keychain
- `install-profile` - Install a provisioning profile
- `cert-info` - Get detailed certificate information

**Usage:**
```bash
# List available certificates
python3 fearn_cert_manager.py list-certs

# List provisioning profiles
python3 fearn_cert_manager.py list-profiles

# Import a certificate
python3 fearn_cert_manager.py import-cert -c certificate.p12 -p "password"

# Install a provisioning profile
python3 fearn_cert_manager.py install-profile -p profile.mobileprovision
```

### 3. **Batch Signer** (`fearn_batch_signer.py`)
Sign multiple IPA files in batch.

**Usage:**
```bash
# Sign all IPAs in a directory
python3 fearn_batch_signer.py -i ./ipa_files -c "iPhone Developer" -o ./signed_ipa

# Recursively sign IPAs in subdirectories
python3 fearn_batch_signer.py -i ./projects -c "iPhone Developer" -o ./signed_ipa -r

# With verbose output
python3 fearn_batch_signer.py -i ./ipa_files -c "iPhone Developer" -o ./signed_ipa -v
```

### 4. **IPA Validator** (`fearn_validator.py`)
Validate IPA structure and integrity.

**Features:**
- Check IPA ZIP structure
- Validate required files and directories
- Validate Info.plist contents
- Verify required keys in app configuration
- Calculate SHA256 checksums

**Usage:**
```bash
# Validate an IPA
python3 fearn_validator.py -i app.ipa

# Validate with checksum
python3 fearn_validator.py -i app.ipa --checksum

# Verbose validation
python3 fearn_validator.py -i app.ipa -v
```

## Requirements

- macOS with Xcode Command Line Tools
- Python 3.6+
- `codesign` utility (part of Xcode)
- `security` command-line tool
- `zip` and `unzip` utilities

## Installation

1. Ensure all Python scripts are executable:
```bash
chmod +x fearn_signer.py
chmod +x fearn_cert_manager.py
chmod +x fearn_batch_signer.py
chmod +x fearn_validator.py
```

2. (Optional) Add to PATH for global access:
```bash
export PATH="$PATH:$(pwd)"
```

## Examples

### Complete Signing Workflow

1. **List available certificates:**
```bash
python3 fearn_cert_manager.py list-certs
```

2. **Validate IPA before signing:**
```bash
python3 fearn_validator.py -i app.ipa
```

3. **Sign the IPA:**
```bash
python3 fearn_signer.py resign -i app.ipa -c "iPhone Developer" -o app-signed.ipa
```

4. **Verify signature:**
```bash
python3 fearn_signer.py verify -i app-signed.ipa
```

### Batch Processing

```bash
# Sign all IPAs in a directory
python3 fearn_batch_signer.py \
  -i ./unsigned_apps \
  -c "iPhone Developer" \
  -o ./signed_apps \
  -v
```

## File Structure

```
Fearn/
├── fearn_signer.py           # Main IPA signer
├── fearn_cert_manager.py     # Certificate management
├── fearn_batch_signer.py     # Batch signing utility
├── fearn_validator.py        # IPA validation
├── FEATURES.md               # This file
├── README.md                 # Installation guide
└── Payload/
    └── Fearn.app/            # Template app bundle
```

## Error Handling

All tools include comprehensive error handling:
- File existence validation
- Permission checking
- Certificate validation
- IPA structure verification
- Detailed error messages

## Logging

All tools support verbose logging:
```bash
python3 fearn_signer.py resign -i app.ipa -c "cert" -o signed.ipa -v
```

## Troubleshooting

### Certificate not found
```bash
# Check available certificates
python3 fearn_cert_manager.py list-certs

# Import missing certificate
python3 fearn_cert_manager.py import-cert -c cert.p12
```

### IPA validation fails
```bash
# Run detailed validation
python3 fearn_validator.py -i app.ipa -v --checksum
```

### Signing fails
1. Verify certificate availability
2. Check IPA structure validity
3. Ensure Xcode tools are installed
4. Check file permissions

## Security Notes

- Certificates are stored in your macOS keychain
- Provisioning profiles are stored in `~/Library/MobileDevice/Provisioning Profiles/`
- All temporary files are cleaned up after signing
- Checksums verify file integrity

## License

MIT
