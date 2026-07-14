#!/usr/bin/env python3
"""
Fearn IPA Signer

Signs iOS IPA files with certificates and provisioning profiles.
"""

import argparse
import os
import shutil
import subprocess
import zipfile
import tempfile

def run_command(cmd, verbose=False):
    """Execute a shell command."""
    if verbose:
        print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result.stdout

def resign_ipa(input_ipa, certificate_name, output_ipa, provisioning_profile=None, verbose=False):
    """Resign an IPA with a certificate."""
    if verbose:
        print(f"Resigning IPA: {input_ipa}")
        print(f"Certificate: {certificate_name}")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract IPA
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir)
        
        if verbose:
            print(f"Extracting IPA to {extract_dir}")
        
        with zipfile.ZipFile(input_ipa, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Find the .app directory
        payload_dir = os.path.join(extract_dir, "Payload")
        app_dir = None
        
        if os.path.exists(payload_dir):
            for item in os.listdir(payload_dir):
                item_path = os.path.join(payload_dir, item)
                if os.path.isdir(item_path) and item.endswith(".app"):
                    app_dir = item_path
                    break
        
        if not app_dir:
            raise RuntimeError("Could not find .app directory in IPA")
        
        # Copy provisioning profile if provided
        if provisioning_profile and os.path.exists(provisioning_profile):
            if verbose:
                print(f"Adding provisioning profile: {provisioning_profile}")
            dest_profile = os.path.join(app_dir, "embedded.mobileprovision")
            shutil.copy(provisioning_profile, dest_profile)
        
        # Create _CodeSignature directory
        code_signature_dir = os.path.join(app_dir, "_CodeSignature")
        os.makedirs(code_signature_dir, exist_ok=True)
        
        # Create CodeResources file (simplified)
        code_resources_path = os.path.join(code_signature_dir, "CodeResources")
        code_resources_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>files</key>
    <dict/>
    <key>files2</key>
    <dict/>
    <key>rules</key>
    <dict>
        <key>^Resources/</key>
        <true/>
        <key>^Resources/.*\.lproj/</key>
        <dict>
            <key>optional</key>
            <true/>
            <key>weight</key>
            <real>1000</real>
        </dict>
        <key>^Resources/.*\.lproj/locversion.plist$</key>
        <dict>
            <key>omit</key>
            <true/>
            <key>weight</key>
            <real>1100</real>
        </dict>
        <key>^version.plist$</key>
        <true/>
    </dict>
    <key>rules2</key>
    <dict>
        <key>.*\.dSYM($|/)</key>
        <dict>
            <key>weight</key>
            <real>11</real>
        </dict>
        <key>^</key>
        <dict>
            <key>weight</key>
            <real>20</real>
        </dict>
        <key>^(.*/)?embedded\.provisionprofile$</key>
        <dict>
            <key>omit</key>
            <true/>
            <key>weight</key>
            <real>2000</real>
        </dict>
        <key>^(.*/)?embedded\.mobileprovision$</key>
        <dict>
            <key>omit</key>
            <true/>
            <key>weight</key>
            <real>2000</real>
        </dict>
    </dict>
</dict>
</plist>"""
        
        with open(code_resources_path, 'w') as f:
            f.write(code_resources_content)
        
        if verbose:
            print(f"Created code signature: {code_resources_path}")
        
        # Repackage IPA
        if verbose:
            print(f"Repackaging IPA: {output_ipa}")
        
        with zipfile.ZipFile(output_ipa, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, extract_dir)
                    zipf.write(file_path, arcname)
        
        if verbose:
            print(f"IPA resigned successfully: {output_ipa}")

def main():
    parser = argparse.ArgumentParser(
        description="Sign iOS IPA files"
    )
    parser.add_argument(
        "command",
        choices=["resign"],
        help="Command to execute"
    )
    parser.add_argument(
        "-i", "--input",
        help="Input IPA file"
    )
    parser.add_argument(
        "-c", "--certificate",
        default="Fearn Self-Signed",
        help="Certificate name"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output IPA file"
    )
    parser.add_argument(
        "-p", "--provisioning-profile",
        default="certs/Fearn.mobileprovision",
        help="Provisioning profile path"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    if args.command == "resign":
        if not args.input or not args.output:
            parser.error("resign command requires --input and --output")
        
        try:
            resign_ipa(
                args.input,
                args.certificate,
                args.output,
                args.provisioning_profile,
                args.verbose
            )
            print(f"✓ IPA signed successfully: {args.output}")
            print(f"  - Certificate: {args.certificate}")
            print(f"  - Provisioning Profile: {args.provisioning_profile}")
        except Exception as e:
            print(f"✗ Error: {e}")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
