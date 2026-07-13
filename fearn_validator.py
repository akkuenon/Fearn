#!/usr/bin/env python3
"""
Fearn IPA Validator - Validate IPA structure and integrity
"""

import os
import sys
import argparse
import zipfile
import plistlib
from pathlib import Path
from typing import List, Tuple
import hashlib

class IPAValidator:
    """Validate IPA files"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.info = []
    
    def log(self, message: str, level: str = 'INFO'):
        """Log messages"""
        if self.verbose or level != 'DEBUG':
            print(f"[{level}] {message}")
    
    def validate_ipa_structure(self, ipa_path: str) -> Tuple[bool, dict]:
        """Validate IPA file structure"""
        try:
            ipa_path = Path(ipa_path)
            if not ipa_path.exists():
                self.errors.append(f"IPA file not found: {ipa_path}")
                return False, {}
            
            if not zipfile.is_zipfile(str(ipa_path)):
                self.errors.append(f"File is not a valid ZIP archive: {ipa_path}")
                return False, {}
            
            self.log(f"Validating IPA: {ipa_path.name}")
            
            result = {'valid': True, 'issues': []}
            
            with zipfile.ZipFile(str(ipa_path), 'r') as zf:
                files = zf.namelist()
                
                # Check for required structure
                has_payload = any(f.startswith('Payload/') for f in files)
                has_app = any(f.endswith('.app/') for f in files)
                
                if not has_payload:
                    self.errors.append("Missing Payload directory")
                    result['valid'] = False
                    result['issues'].append('Missing Payload directory')
                
                if not has_app:
                    self.errors.append("No .app bundle found")
                    result['valid'] = False
                    result['issues'].append('No .app bundle found')
                
                # Check for required files
                required_files = ['Info.plist', 'PkgInfo', '_CodeSignature/']
                
                for app_file in files:
                    if '.app/' in app_file:
                        for required in required_files:
                            if not any(f.endswith(f'.app/{required}') or 
                                     f.endswith(f'.app/{required}') 
                                     for f in files if '.app/' in f):
                                self.warnings.append(f"Potentially missing: {required}")
                                result['issues'].append(f'Missing {required}')
                        break
                
                self.info.append(f"Total files in archive: {len(files)}")
                result['file_count'] = len(files)
        
        except Exception as e:
            self.errors.append(f"Error validating IPA: {e}")
            return False, {}
        
        return result['valid'], result
    
    def validate_info_plist(self, ipa_path: str) -> Tuple[bool, dict]:
        """Validate Info.plist contents"""
        try:
            ipa_path = Path(ipa_path)
            
            with zipfile.ZipFile(str(ipa_path), 'r') as zf:
                # Find Info.plist
                info_plists = [f for f in zf.namelist() if f.endswith('Info.plist')]
                
                if not info_plists:
                    self.errors.append("Info.plist not found")
                    return False, {}
                
                info_plist_path = info_plists[0]
                self.log(f"Validating Info.plist: {info_plist_path}")
                
                with zf.open(info_plist_path) as f:
                    plist = plistlib.load(f)
                
                result = {'valid': True, 'plist': {}}
                
                # Check required keys
                required_keys = ['CFBundleIdentifier', 'CFBundleExecutable', 'CFBundleVersion']
                
                for key in required_keys:
                    if key not in plist:
                        self.warnings.append(f"Missing key: {key}")
                    else:
                        result['plist'][key] = plist[key]
                
                self.info.append(f"Bundle ID: {plist.get('CFBundleIdentifier', 'Unknown')}")
                self.info.append(f"Version: {plist.get('CFBundleShortVersionString', 'Unknown')}")
                self.info.append(f"Build: {plist.get('CFBundleVersion', 'Unknown')}")
                
                return True, result
        
        except Exception as e:
            self.errors.append(f"Error validating Info.plist: {e}")
            return False, {}
    
    def calculate_checksum(self, ipa_path: str) -> str:
        """Calculate SHA256 checksum of IPA file"""
        try:
            ipa_path = Path(ipa_path)
            sha256_hash = hashlib.sha256()
            
            with open(str(ipa_path), 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b''):
                    sha256_hash.update(byte_block)
            
            checksum = sha256_hash.hexdigest()
            self.info.append(f"SHA256: {checksum}")
            return checksum
        except Exception as e:
            self.errors.append(f"Error calculating checksum: {e}")
            return ""
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "="*50)
        print("IPA Validation Report")
        print("="*50)
        
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  ✗ {error}")
        
        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if self.info:
            print("\nInformation:")
            for info in self.info:
                print(f"  ℹ {info}")
        
        print("="*50)


def main():
    parser = argparse.ArgumentParser(
        description='Fearn IPA Validator - Validate IPA structure and integrity'
    )
    
    parser.add_argument('-i', '--input', required=True, help='IPA file to validate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--checksum', action='store_true', help='Calculate file checksum')
    
    args = parser.parse_args()
    
    validator = IPAValidator(verbose=args.verbose)
    
    try:
        # Validate structure
        struct_valid, struct_result = validator.validate_ipa_structure(args.input)
        
        # Validate Info.plist
        plist_valid, plist_result = validator.validate_info_plist(args.input)
        
        # Calculate checksum if requested
        if args.checksum:
            validator.calculate_checksum(args.input)
        
        # Print report
        validator.print_report()
        
        # Exit code based on validation
        return 0 if (struct_valid and plist_valid and not validator.errors) else 1
    
    except KeyboardInterrupt:
        validator.log("Operation cancelled", 'WARN')
        return 130
    except Exception as e:
        validator.log(f"Unexpected error: {e}", 'ERROR')
        return 1


if __name__ == '__main__':
    sys.exit(main())
