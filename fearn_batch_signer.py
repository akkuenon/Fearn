#!/usr/bin/env python3
"""
Fearn Batch Signer - Batch sign multiple IPA files
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List
from fearn_signer import IPASigner

class BatchSigner:
    """Handle batch signing of multiple IPAs"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.stats = {
            'total': 0,
            'successful': 0,
            'failed': 0
        }
    
    def log(self, message: str, level: str = 'INFO'):
        """Log messages"""
        if self.verbose or level != 'DEBUG':
            print(f"[{level}] {message}")
    
    def find_ipa_files(self, directory: str, recursive: bool = False) -> List[Path]:
        """Find all IPA files in a directory"""
        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                self.log(f"Directory not found: {directory}", 'ERROR')
                return []
            
            pattern = '**/*.ipa' if recursive else '*.ipa'
            ipa_files = list(dir_path.glob(pattern))
            
            self.log(f"Found {len(ipa_files)} IPA file(s)")
            for ipa in ipa_files:
                self.log(f"  - {ipa.name}")
            
            return ipa_files
        except Exception as e:
            self.log(f"Error finding IPA files: {e}", 'ERROR')
            return []
    
    def sign_batch(self, input_dir: str, certificate: str, output_dir: str,
                   recursive: bool = False, identity: str = None) -> bool:
        """Sign all IPAs in a batch"""
        try:
            ipa_files = self.find_ipa_files(input_dir, recursive)
            
            if not ipa_files:
                self.log("No IPA files found", 'ERROR')
                return False
            
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            self.stats['total'] = len(ipa_files)
            
            self.log(f"Starting batch signing of {self.stats['total']} IPA file(s)...")
            
            for idx, ipa_file in enumerate(ipa_files, 1):
                self.log(f"\n[{idx}/{self.stats['total']}] Processing: {ipa_file.name}")
                
                output_file = output_path / f"{ipa_file.stem}-signed.ipa"
                
                signer = IPASigner(verbose=self.verbose)
                try:
                    if signer.resign_ipa(str(ipa_file), certificate, str(output_file), identity):
                        self.stats['successful'] += 1
                        self.log(f"✓ Successfully signed: {output_file.name}")
                    else:
                        self.stats['failed'] += 1
                        self.log(f"✗ Failed to sign: {ipa_file.name}", 'ERROR')
                except Exception as e:
                    self.stats['failed'] += 1
                    self.log(f"✗ Error signing {ipa_file.name}: {e}", 'ERROR')
            
            self.print_summary()
            return self.stats['failed'] == 0
        except Exception as e:
            self.log(f"Error in batch signing: {e}", 'ERROR')
            return False
    
    def print_summary(self):
        """Print batch operation summary"""
        self.log("\n" + "="*50)
        self.log("Batch Signing Summary", 'INFO')
        self.log("="*50)
        self.log(f"Total IPAs processed: {self.stats['total']}")
        self.log(f"Successfully signed:  {self.stats['successful']}")
        self.log(f"Failed:               {self.stats['failed']}")
        self.log("="*50)


def main():
    parser = argparse.ArgumentParser(
        description='Fearn Batch Signer - Batch sign multiple IPA files'
    )
    
    parser.add_argument('-i', '--input', required=True, help='Input directory containing IPA files')
    parser.add_argument('-c', '--certificate', required=True, help='Certificate to sign with')
    parser.add_argument('-o', '--output', required=True, help='Output directory for signed IPAs')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursively search subdirectories')
    parser.add_argument('--identity', help='Signing identity (optional)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    batch_signer = BatchSigner(verbose=args.verbose)
    
    try:
        success = batch_signer.sign_batch(
            args.input,
            args.certificate,
            args.output,
            args.recursive,
            args.identity
        )
        return 0 if success else 1
    except KeyboardInterrupt:
        batch_signer.log("Operation cancelled", 'WARN')
        return 130
    except Exception as e:
        batch_signer.log(f"Unexpected error: {e}", 'ERROR')
        return 1


if __name__ == '__main__':
    sys.exit(main())
