# IPA File Format Documentation

## What is an IPA?

An IPA (iPhone Application Archive) is a ZIP archive containing an iOS application and its resources. It follows Apple's app distribution format.

## Required Components

### 1. Payload Directory
```
Payload/
└── YourApp.app/
    ├── Info.plist                  (Required)
    ├── embedded.mobileprovision    (Required for distribution)
    ├── PkgInfo                     (Required)
    ├── YourApp                     (Binary executable - Required)
    ├── _CodeSignature/
    │   └── CodeResources           (Required for signed apps)
    └── Resources/
        ├── Base.lproj/             (Localizable resources)
        ├── Assets.car              (Images and assets)
        └── ...other resources
```

### 2. iTunes Metadata (Optional but Common)
```
iTunesMetadata.plist
```

## File Descriptions

### Info.plist
XML property list containing:
- **CFBundleIdentifier**: Unique app identifier (e.g., com.company.appname)
- **CFBundleExecutable**: Name of the executable binary
- **CFBundleShortVersionString**: User-visible version (e.g., 1.0)
- **CFBundleVersion**: Build number
- **CFBundlePackageType**: Always "APPL" for apps
- **LSRequiresIPhoneOS**: Boolean indicating iOS requirement
- Other capabilities and requirements

### embedded.mobileprovision
Binary provisioning profile containing:
- Team ID
- App entitlements
- Supported devices (if dev profile)
- Expiration date
- Certificates

### PkgInfo
Simple 4-byte file:
```
APPL????
```
First 4 bytes: "APPL" (application type)
Last 4 bytes: "????" (reserved)

### _CodeSignature/CodeResources
XML plist containing:
- SHA1 hashes of all files (for backward compatibility)
- SHA256 hashes of all files (modern)
- Code signing rules and weights
- Optional and weighted files

### Executable Binary (e.g., Fearn)
The compiled Mach-O binary:
- Must be an ARM64 or ARMv7 binary
- Must be code-signed
- Named to match CFBundleExecutable in Info.plist

## Standard Directory Structure

```
MyApp.app/
├── Info.plist                          - App configuration
├── PkgInfo                             - Package identifier
├── MyApp                               - Executable binary
├── embedded.mobileprovision            - Provisioning profile
├── _CodeSignature/
│   └── CodeResources                  - Code signature manifest
├── Base.lproj/                        - Default language resources
│   ├── Main.storyboard                - Main UI (compiled)
│   └── Localizable.strings            - Localized strings
├── en.lproj/                          - English localization
├── Assets.car                         - Compiled asset catalog
├── Frameworks/                        - Embedded frameworks (optional)
├── Plugins/                           - Embedded plugins (optional)
└── Watch/                             - Watch app bundle (optional)
```

## Creating an IPA from Source

### Step 1: Build the App
```bash
xcodebuild -scheme MyApp -configuration Release
```

### Step 2: Locate the .app
```bash
find ~/Library/Developer/Xcode/DerivedData -name "*.app" -type d
```

### Step 3: Create IPA Structure
```bash
mkdir -p MyApp.ipa/Payload
cp -r MyApp.app MyApp.ipa/Payload/
```

### Step 4: Add Metadata
```bash
cp iTunesMetadata.plist MyApp.ipa/
```

### Step 5: Create ZIP Archive
```bash
cd MyApp.ipa
zip -r ../MyApp.ipa Payload iTunesMetadata.plist
```

## Code Signing

### Automatic Signing
```bash
codesign -fs - Payload/MyApp.app
```

### Manual Signing with Certificate
```bash
codesign -fs "iPhone Developer: Name (XXXXXXXX)" Payload/MyApp.app
```

### Verify Signature
```bash
codesign -v Payload/MyApp.app
```

## Testing an IPA

### Install on Device via Xcode
```bash
xcode-select --install
ios-deploy -b MyApp.ipa
```

### Install via Apple Configurator 2
1. Connect device
2. Open Apple Configurator 2
3. Select device
4. Drag and drop IPA file

### Validate IPA
```bash
xcodebuild -validateProductName MyApp.ipa
```
