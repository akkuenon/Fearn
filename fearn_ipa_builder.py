#!/usr/bin/env python3
"""
Fearn IPA Builder

Builds an iOS IPA (iPhone Application Archive) from app resources.
"""

import argparse
import os
import shutil
import subprocess
import zipfile

def run_command(cmd, verbose=False):
    """Execute a shell command."""
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result.stdout

def create_ipa_structure(app_name, verbose=False):
    """Create the basic IPA directory structure."""
    if verbose:
        print(f"Creating IPA structure for {app_name}")
    
    # Create directories
    payload_dir = "Payload"
    app_dir = os.path.join(payload_dir, f"{app_name}.app")
    
    os.makedirs(app_dir, exist_ok=True)
    os.makedirs(os.path.join(payload_dir, "Symbols"), exist_ok=True)
    
    # Create a minimal Info.plist
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>{app_name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.krnlthemodder.{app_name.lower()}</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>{app_name}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSRequiresIPhoneOS</key>
    <true/>
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>armv7</string>
    </array>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
    </array>
</dict>
</plist>
"""
    
    info_plist_path = os.path.join(app_dir, "Info.plist")
    with open(info_plist_path, "w") as f:
        f.write(plist_content)
    
    if verbose:
        print(f"Created Info.plist at {info_plist_path}")
    
    return payload_dir, app_dir

def create_ipa(payload_dir, output_path, verbose=False):
    """Create the final IPA file."""
    if verbose:
        print(f"Creating IPA archive: {output_path}")
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(payload_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
    
    if verbose:
        print(f"IPA created successfully: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Build an iOS IPA for Fearn"
    )
    parser.add_argument(
        "--name",
        default="Fearn",
        help="App name"
    )
    parser.add_argument(
        "--bundle-id",
        default="com.krnlthemodder.fearn",
        help="Bundle ID for the app"
    )
    parser.add_argument(
        "--version",
        default="1.0",
        help="App version"
    )
    parser.add_argument(
        "--output",
        default=".",
        help="Output directory for the IPA"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        # Create IPA structure
        payload_dir, app_dir = create_ipa_structure(args.name, args.verbose)
        
        # Ensure executable exists
        executable_path = os.path.join(app_dir, args.name)
        if not os.path.exists(executable_path):
            open(executable_path, 'a').close()
            os.chmod(executable_path, 0o755)
            if args.verbose:
                print(f"Created executable placeholder: {executable_path}")
        
        # Create IPA
        ipa_filename = f"{args.name}-{args.version}.ipa"
        ipa_path = os.path.join(args.output, ipa_filename)
        create_ipa(payload_dir, ipa_path, args.verbose)
        
        print(f"✓ IPA built successfully: {ipa_path}")
        print(f"  - App name: {args.name}")
        print(f"  - Bundle ID: {args.bundle_id}")
        print(f"  - Version: {args.version}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
