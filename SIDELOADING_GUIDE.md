# Fearn IPA Sideloading - Complete Setup Guide

## Prerequisites

- Python 3.7+
- OpenSSL (for certificate generation)
- zip utility (or Python will use built-in)

## Installation

```bash
bash install.sh
```

## Quick Start: Build & Sign

### 1. Generate Certificates & Provisioning Profile

```bash
python3 fearn_cert_provisioning_generator.py \
    --bundle-id "com.krnlthemodder.fearn" \
    --team-id "XXXXXXXXXX" \
    --name "Fearn" \
    --verbose
```

This creates in `certs/`:
- `Fearn.cer` - Self-signed certificate
- `Fearn.key` - Private key
- `Fearn.p12` - PKCS12 (Password: `fearn123`)
- `Fearn.mobileprovision` - Provisioning profile with get-task-allow

### 2. Build IPA

```bash
python3 fearn_ipa_builder.py \
    --name "Fearn" \
    --bundle-id "com.krnlthemodder.fearn" \
    --version "1.0" \
    --output "." \
    --verbose
```

### 3. Sign IPA

```bash
python3 fearn_signer.py resign \
    -i Fearn-1.0.ipa \
    -c "Fearn Self-Signed" \
    -o Fearn-1.0-signed.ipa \
    --verbose
```

### Or Use Complete Setup Script

```bash
bash setup_and_build.sh
```

## Sideloading Entitlements

The generated provisioning profile includes critical entitlements:

| Entitlement | Purpose |
|---|---|
| `com.apple.get-task-allow` | Enable debugging & attach LLDB |
| `get-task-allow` | Legacy debugging support |
| `keychain-access-groups` | Access keychain |
| `aps-environment: development` | Development push notifications |
| `beta-reports-active` | Beta testing support |

## Installing on Device

### Method 1: Xcode (Easiest)

1. Import `Fearn.p12` into Keychain Access
2. Drag signed IPA to Xcode's Devices window

### Method 2: Command Line (ideviceinstaller)

```bash
ideviceinstaller -i Fearn-1.0-signed.ipa
```

### Method 3: Cydia Impactor (Legacy)

1. Install Cydia Impactor
2. Drag signed IPA to Cydia Impactor
3. Enter Apple ID (temporary provisioning)

## File Structure

```
Fearn/
├── Payload/
│   └── Fearn.app/
│       ├── Info.plist
│       ├── Fearn (executable)
│       ├── PkgInfo
│       ├── embedded.mobileprovision
│       └── _CodeSignature/
├── certs/
│   ├── Fearn.cer
│   ├── Fearn.key
│   ├── Fearn.p12
│   └── Fearn.mobileprovision
├── fearn_ipa_builder.py
├── fearn_signer.py
├── fearn_cert_provisioning_generator.py
└── setup_and_build.sh
```

## Troubleshooting

### "No executable found" Error
- Check that `Payload/Fearn.app/Fearn` exists
- Run setup script to auto-create placeholder

### "Invalid provisioning profile" Error
- Ensure `Fearn.mobileprovision` is in `certs/`
- Regenerate with: `python3 fearn_cert_provisioning_generator.py`

### Signing fails on device
- Import `Fearn.p12` (password: `fearn123`) into Keychain
- Trust the certificate in Keychain

### Can't attach debugger (LLDB)
- Verify `com.apple.get-task-allow` is in provisioning profile
- Check build log for get-task-allow confirmation

## Advanced

### Custom Bundle ID

```bash
python3 fearn_ipa_builder.py \
    --name "MyApp" \
    --bundle-id "com.example.myapp" \
    --version "2.0"
```

### Custom Team ID

```bash
python3 fearn_cert_provisioning_generator.py \
    --team-id "YOURTMID" \
    --bundle-id "com.yourcompany.app"
```

## License

See LICENSE file

## Support

For issues, check GitHub: https://github.com/krn11ikiowo/Fearn
