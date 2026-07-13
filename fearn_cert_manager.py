#!/usr/bin/env python3
"""
Fearn Certificate Manager - Manage iOS certificates and provisioning profiles
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional
import json

class CertificateManager:
    """Manage certificates and provisioning profiles"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.keychain_path = Path.home() / 'Library' / 'Keychains' / 'login.keychain-db'
    
    def log(self, message: str, level: str = 'INFO'):
        """Log messages"""
        if self.verbose or level != 'DEBUG':
            print(f"[{level}] {message}")
    
    def list_certificates(self) -> List[str]:
        """List all available signing certificates"""
        try:
            self.log("Fetching available certificates...")
            result = subprocess.run(
                ['security', 'find-identity', '-v', '-p', 'codesigning', str(self.keychain_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.log("Failed to fetch certificates", 'ERROR')
                return []
            
            certificates = []
            for line in result.stdout.strip().split('\n'):
                if 'iPhone' in line:
                    certificates.append(line.strip())
            
            if certificates:
                self.log(f"Found {len(certificates)} certificate(s)")
                for cert in certificates:
                    print(cert)
            else:
                self.log("No certificates found", 'WARN')
            
            return certificates
        except Exception as e:
            self.log(f"Error listing certificates: {e}", 'ERROR')
            return []
    
    def list_provisioning_profiles(self) -> List[dict]:
        """List all provisioning profiles"""
        try:
            self.log("Fetching provisioning profiles...")
            profiles_dir = Path.home() / 'Library' / 'MobileDevice' / 'Provisioning Profiles'
            
            if not profiles_dir.exists():
                self.log(f"Provisioning profiles directory not found: {profiles_dir}", 'WARN')
                return []
            
            profiles = []
            for profile_file in profiles_dir.glob('*.mobileprovision'):
                profiles.append({
                    'path': str(profile_file),
                    'name': profile_file.name,
                    'timestamp': os.path.getmtime(profile_file)
                })
            
            self.log(f"Found {len(profiles)} provisioning profile(s)")
            for profile in profiles:
                print(f"  - {profile['name']}")
            
            return profiles
        except Exception as e:
            self.log(f"Error listing provisioning profiles: {e}", 'ERROR')
            return []
    
    def import_certificate(self, cert_path: str, password: Optional[str] = None) -> bool:
        """Import a certificate into keychain"""
        try:
            cert_path = Path(cert_path)
            if not cert_path.exists():
                self.log(f"Certificate file not found: {cert_path}", 'ERROR')
                return False
            
            self.log(f"Importing certificate: {cert_path}")
            
            cmd = ['security', 'import', str(cert_path), '-k', str(self.keychain_path)]
            if password:
                cmd.extend(['-P', password])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("Certificate imported successfully")
                return True
            else:
                self.log(f"Failed to import certificate: {result.stderr}", 'ERROR')
                return False
        except Exception as e:
            self.log(f"Error importing certificate: {e}", 'ERROR')
            return False
    
    def install_provisioning_profile(self, profile_path: str) -> bool:
        """Install a provisioning profile"""
        try:
            profile_path = Path(profile_path)
            if not profile_path.exists():
                self.log(f"Profile file not found: {profile_path}", 'ERROR')
                return False
            
            dest_dir = Path.home() / 'Library' / 'MobileDevice' / 'Provisioning Profiles'
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            dest_path = dest_dir / profile_path.name
            
            self.log(f"Installing provisioning profile: {profile_path.name}")
            import shutil
            shutil.copy2(str(profile_path), str(dest_path))
            
            self.log(f"Profile installed: {dest_path}")
            return True
        except Exception as e:
            self.log(f"Error installing profile: {e}", 'ERROR')
            return False
    
    def get_certificate_info(self, certificate_id: str) -> Optional[dict]:
        """Get detailed information about a certificate"""
        try:
            self.log(f"Fetching certificate info: {certificate_id}")
            result = subprocess.run(
                ['security', 'find-certificate', '-c', certificate_id, str(self.keychain_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("Certificate information retrieved")
                print(result.stdout)
                return result.stdout
            else:
                self.log("Failed to retrieve certificate information", 'ERROR')
                return None
        except Exception as e:
            self.log(f"Error getting certificate info: {e}", 'ERROR')
            return None


def main():
    parser = argparse.ArgumentParser(
        description='Fearn Certificate Manager - Manage iOS certificates and provisioning profiles'
    )
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List certificates
    list_certs = subparsers.add_parser('list-certs', help='List available certificates')
    
    # List provisioning profiles
    list_profiles = subparsers.add_parser('list-profiles', help='List provisioning profiles')
    
    # Import certificate
    import_cert = subparsers.add_parser('import-cert', help='Import a certificate')
    import_cert.add_argument('-c', '--cert', required=True, help='Certificate file path')
    import_cert.add_argument('-p', '--password', help='Certificate password (optional)')
    
    # Install profile
    install_prof = subparsers.add_parser('install-profile', help='Install a provisioning profile')
    install_prof.add_argument('-p', '--profile', required=True, help='Profile file path')
    
    # Certificate info
    cert_info = subparsers.add_parser('cert-info', help='Get certificate information')
    cert_info.add_argument('-i', '--id', required=True, help='Certificate ID')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    manager = CertificateManager(verbose=args.verbose)
    
    try:
        if args.command == 'list-certs':
            manager.list_certificates()
        elif args.command == 'list-profiles':
            manager.list_provisioning_profiles()
        elif args.command == 'import-cert':
            success = manager.import_certificate(args.cert, args.password)
            return 0 if success else 1
        elif args.command == 'install-profile':
            success = manager.install_provisioning_profile(args.profile)
            return 0 if success else 1
        elif args.command == 'cert-info':
            manager.get_certificate_info(args.id)
        
        return 0
    except KeyboardInterrupt:
        manager.log("Operation cancelled", 'WARN')
        return 130
    except Exception as e:
        manager.log(f"Unexpected error: {e}", 'ERROR')
        return 1


if __name__ == '__main__':
    sys.exit(main())
