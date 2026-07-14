# Fearn Certificate Release - V-1.7.0 build 6

## Release Information
- **Version**: V-1.7.0 build 6
- **Release Date**: 2026-07-14
- **Type**: Certificate Release

## Contents
This release contains all certificates and provisioning profiles required for building and signing Fearn iOS applications.

### Certificate Files
- `Fearn.cer` - Self-signed certificate
- `Fearn.key` - Private key
- `Fearn.p12` - PKCS12 certificate bundle (Password: `fearn123`)
- `Fearn.mobileprovision` - iOS provisioning profile with debug entitlements

## Installation Instructions

### 1. Extract the Certificate Archive
```bash
unzip Fearn-Certificates-V-1.7.0-build6.zip -d certs/
```

### 2. Import Certificate to Keychain
```bash
python3 fearn_cert_manager.py import-cert -c certs/Fearn.p12 -p fearn123
```

### 3. Install Provisioning Profile
```bash
python3 fearn_cert_manager.py install-profile -p certs/Fearn.mobileprovision
```

## Usage

### Generate Certificates
```bash
python3 fearn_cert_provisioning_generator.py \
    --bundle-id "com.krnlthemodder.fearn" \
    --team-id "XXXXXXXXXX" \
    --name "Fearn"
```

### Sign IPA
```bash
python3 fearn_signer.py resign \
    -i Fearn-1.0.ipa \
    -c "Fearn Self-Signed" \
    -o Fearn-1.0-signed.ipa
```

### Batch Sign Multiple IPAs
```bash
python3 fearn_batch_signer.py \
    -i ./ipas \
    -c "Fearn Self-Signed" \
    -o ./signed_ipas
```

## Entitlements Included
- `com.apple.get-task-allow` - Enable debugging
- `get-task-allow` - Legacy debugging support
- `keychain-access-groups` - Keychain access
- `aps-environment: development` - Development push notifications
- `beta-reports-active` - Beta testing support

## Security Notes
- Keep the private key (`Fearn.key`) secure
- The P12 certificate password is: `fearn123`
- Only distribute certificates to authorized team members
- Certificate validity: 365 days from generation

## Support
For certificate management issues, use:
```bash
python3 fearn_cert_manager.py --help
```

---
**Build**: 6  
**Status**: Release Ready  
**Checksum**: Available in release assets
