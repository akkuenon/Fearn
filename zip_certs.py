#!/usr/bin/env python3
"""
Zip up certificate files (.p12 and .mobileprovision)
Run this script to create a compressed archive of your certificates.
"""

import os
import zipfile
import glob
from datetime import datetime

def zip_certificates(output_filename="certs_backup.zip", verbose=True):
    """
    Zip all .p12 and .mobileprovision files in the current directory
    and subdirectories.
    
    Args:
        output_filename (str): Name of the output zip file
        verbose (bool): Print progress messages
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    # Find all certificate files
    cert_patterns = ['*.p12', '*.mobileprovision', '**/*.p12', '**/*.mobileprovision']
    cert_files = []
    
    for pattern in cert_patterns:
        cert_files.extend(glob.glob(pattern, recursive=True))
    
    # Remove duplicates
    cert_files = list(set(cert_files))
    
    if not cert_files:
        if verbose:
            print("❌ No certificate files found (.p12 or .mobileprovision)")
        return False
    
    if verbose:
        print(f"📦 Found {len(cert_files)} certificate file(s):")
        for cert_file in cert_files:
            print(f"   - {cert_file}")
    
    try:
        with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for cert_file in cert_files:
                if os.path.exists(cert_file):
                    zipf.write(cert_file)
                    if verbose:
                        print(f"✅ Added: {cert_file}")
        
        file_size = os.path.getsize(output_filename)
        if verbose:
            print(f"\n✨ Successfully created: {output_filename} ({file_size} bytes)")
        return True
    
    except Exception as e:
        if verbose:
            print(f"❌ Error creating zip file: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Zip certificate files (.p12 and .mobileprovision)"
    )
    parser.add_argument(
        "-o", "--output",
        default="certs_backup.zip",
        help="Output zip filename (default: certs_backup.zip)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output messages"
    )
    
    args = parser.parse_args()
    
    success = zip_certificates(
        output_filename=args.output,
        verbose=not args.quiet
    )
    
    exit(0 if success else 1)
