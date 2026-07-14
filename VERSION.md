# Fearn v2.0.0-beta1

## Release Date
July 14, 2026

## Major Features

### 🎯 Entitlement Management System
- **Dynamic Entitlement Editor**: Modify app entitlements directly in the UI without re-signing
- **Entitlement Templates**: Pre-configured templates for common entitlements (iCloud, HealthKit, HomeKit, etc.)
- **Entitlement Validation**: Automatic validation to prevent incompatible entitlement combinations
- **Entitlement Profiles**: Save and load entitlement configurations for quick application

### 🔐 Enhanced Security
- **Certificate Chain Validation**: Verify complete certificate chain integrity
- **Revocation Check**: Check if certificates are on revocation lists
- **Secure Entitlement Signing**: Sign entitlements with additional verification layers
- **Audit Logging**: Complete logging of all entitlement modifications

### 📦 Advanced Sideloading
- **Batch Entitlement Processing**: Apply entitlements to multiple apps at once
- **Dependency Resolution**: Automatically resolve and manage app dependencies
- **Conflict Detection**: Identify conflicting entitlements before application
- **Rollback Support**: Revert to previous entitlement configurations

### 🎨 UI Improvements
- **Entitlement Browser**: Visual interface for exploring all available entitlements
- **Diff Viewer**: Compare entitlements before and after modifications
- **Dark Mode Support**: Full dark mode implementation
- **Real-time Validation**: Instant feedback on entitlement changes

### 📱 App Library
- **Curated App Collection**: Pre-configured sideloading apps ready for deployment
- **App Metadata**: Detailed information about each app including version and requirements
- **Auto-installation**: One-click app installation with automatic configuration
- **Update Manager**: Check and manage app updates

## Breaking Changes
- Removed legacy XML-based entitlement format
- Certificate format now requires PKCS#12 with encryption

## Known Issues
- Entitlement diff viewer may take longer for large configurations
- Some legacy provisioning profiles may require manual updates

## Installation
See INSTALLATION.md for upgrade instructions from v1.x
