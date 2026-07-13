# Fearn - IPA Template

This repository contains a complete IPA (iPhone Application Archive) template structure for iOS app development and signing.

## Directory Structure

```
Fearn/
├── Payload/
│   └── Fearn.app/
│       ├── Info.plist                 # App configuration and metadata
│       ├── embedded.mobileprovision   # Provisioning profile
│       ├── PkgInfo                    # Package type identifier
│       ├── Base.lproj/
│       │   └── Main.storyboard        # Main UI storyboard
│       └── _CodeSignature/
│           └── CodeResources          # Code signature manifest
├── iTunesMetadata.plist               # iTunes metadata
└── README.md                          # This file
```

## IPA Structure Explanation

### Payload Directory
- **Required**: Contains the `.app` bundle
- **Fearn.app**: The main application bundle

### Info.plist
- Contains app metadata (bundle ID, version, supported devices, etc.)
- **Bundle ID**: `com.krnlthemodder.fearn`
- **Version**: 1.0 (CFBundleShortVersionString)
- **Build**: 1 (CFBundleVersion)

### embedded.mobileprovision
- Provisioning profile for app signing
- Contains entitlements and team ID information
- **Note**: Replace `XXXXXXXXXX` with your Team ID

### PkgInfo
- Identifies the package type as "APPL" (application)
- Always contains: `APPL????`

### _CodeSignature/CodeResources
- Code signature manifest
- Contains SHA1 and SHA256 hashes of app resources
- **Note**: Hashes are placeholders and need to be calculated

### iTunesMetadata.plist
- Metadata for iTunes/App Store distribution

## How to Use This Template

1. **Replace Placeholders**:
   - Update `XXXXXXXXXX` in `embedded.mobileprovision` with your Apple Team ID
   - Update bundle ID if needed (change `com.krnlthemodder.fearn` to your app's bundle ID)

2. **Add Your App Binary**:
   - Create a compiled binary and place it at `Payload/Fearn.app/Fearn`

3. **Sign the App**:
   ```bash
   codesign -fs - Payload/Fearn.app
   ```

4. **Create IPA Archive**:
   ```bash
   zip -r Fearn.ipa Payload iTunesMetadata.plist
   ```

## Requirements

- macOS with Xcode Command Line Tools installed
- Apple Developer Account (for provisioning profiles and certificates)
- Valid signing certificate and provisioning profile

## License

MIT
