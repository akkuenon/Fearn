#!/usr/bin/env python3
"""
Fearn IPA Signer - iOS IPA file signing and management utility
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple

class IPASigner:
    """Main IPA signing class"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.temp_dir = Path('.ipa_temp')
    
    def log(self, message: str, level: str = 'INFO'):
        """Log messages"""
        if self.verbose or level != 'DEBUG':
            print(f"[{level}] {message}")
    
    def extract_ipa(self, ipa_path: str) -> bool:
        """Extract IPA archive"""
        try:
            ipa_path = Path(ipa_path)
            if not ipa_path.exists():
                self.log(f"IPA file not found: {ipa_path}", 'ERROR')
                return False
            
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            
            self.temp_dir.mkdir()
            
            self.log(f"Extracting IPA: {ipa_path}")
            subprocess.run(['unzip', '-q', str(ipa_path), '-d', str(self.temp_dir)], check=True)
            self.log("IPA extracted successfully")
            return True
        except Exception as e:
            self.log(f"Failed to extract IPA: {e}", 'ERROR')
            return False
    
    def sign_app(self, certificate: str, identity: Optional[str] = None) -> bool:
        """Sign the extracted app bundle"""
        try:
            app_path = self.temp_dir / 'Payload' / '*.app'
            app_dirs = list(self.temp_dir.glob('Payload/*.app'))
            
            if not app_dirs:
                self.log("No .app bundle found in Payload directory", 'ERROR')
                return False
            
            app_path = app_dirs[0]
            self.log(f"Signing app bundle: {app_path.name}")
            
            cmd = ['codesign', '-fs', certificate]
            if identity:
                cmd = ['codesign', '-fs', identity]
            cmd.append(str(app_path))
            
            subprocess.run(cmd, check=True, capture_output=True)
            self.log("App signed successfully")
            return True
        except Exception as e:
            self.log(f"Failed to sign app: {e}", 'ERROR')
            return False
    
    def verify_signature(self) -> bool:
        """Verify the code signature of the app"""
        try:
            app_dirs = list(self.temp_dir.glob('Payload/*.app'))
            if not app_dirs:
                self.log("No .app bundle found", 'ERROR')
                return False
            
            app_path = app_dirs[0]
            self.log(f"Verifying signature for: {app_path.name}")
            
            result = subprocess.run(
                ['codesign', '-v', str(app_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("Signature verification passed")
                print(result.stdout)
                return True
            else:
                self.log("Signature verification failed", 'ERROR')
                print(result.stderr)
                return False
        except Exception as e:
            self.log(f"Failed to verify signature: {e}", 'ERROR')
            return False
    
    def create_ipa(self, output_path: str) -> bool:
        """Create new IPA from modified contents"""
        try:
            output_path = Path(output_path)
            self.log(f"Creating IPA: {output_path}")
            
            # Create zip archive
            subprocess.run(
                ['zip', '-r', '-q', str(output_path), '.'],
                cwd=str(self.temp_dir),
                check=True
            )
            
            self.log(f"IPA created successfully: {output_path}")
            return True
        except Exception as e:
            self.log(f"Failed to create IPA: {e}", 'ERROR')
            return False
    
    def resign_ipa(self, ipa_path: str, certificate: str, output_path: str, 
                   identity: Optional[str] = None) -> bool:
        """Complete resign workflow"""
        try:
            self.log("Starting IPA re-signing process...")
            
            if not self.extract_ipa(ipa_path):
                return False
            
            if not self.sign_app(certificate, identity):
                return False
            
            if not self.verify_signature():
                self.log("Warning: Signature verification failed, but continuing...", 'WARN')
            
            if not self.create_ipa(output_path):
                return False
            
            self.log("IPA re-signing completed successfully!")
            return True
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self.log("Temporary files cleaned up")
    
    def get_app_info(self) -> Optional[dict]:
        """Extract and display app information"""
        try:
            app_dirs = list(self.temp_dir.glob('Payload/*.app'))
            if not app_dirs:
                self.log("No .app bundle found", 'ERROR')
                return None
            
            app_path = app_dirs[0]
            info_plist = app_path / 'Info.plist'
            
            if not info_plist.exists():
                self.log("Info.plist not found", 'ERROR')
                return None
            
            result = subprocess.run(
                ['plutil', '-p', str(info_plist)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("App Information:")
                print(result.stdout)
                return result.stdout
            else:
                self.log("Failed to read Info.plist", 'ERROR')
                return None
        except Exception as e:
            self.log(f"Failed to get app info: {e}", 'ERROR')
            return None


def main():
    parser = argparse.ArgumentParser(
        description='Fearn IPA Signer - iOS IPA file signing utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Re-sign an IPA with a certificate
  %(prog)s resign -i app.ipa -c "iPhone Developer" -o app-signed.ipa
  
  # Extract an IPA
  %(prog)s extract -i app.ipa
  
  # Verify signature
  %(prog)s verify -i app.ipa
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Resign command
    resign_parser = subparsers.add_parser('resign', help='Re-sign an IPA file')
    resign_parser.add_argument('-i', '--input', required=True, help='Input IPA file')
    resign_parser.add_argument('-c', '--certificate', required=True, help='Certificate to sign with')
    resign_parser.add_argument('-o', '--output', required=True, help='Output IPA file')
    resign_parser.add_argument('--identity', help='Signing identity (optional)')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract an IPA file')
    extract_parser.add_argument('-i', '--input', required=True, help='Input IPA file')
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify IPA signature')
    verify_parser.add_argument('-i', '--input', required=True, help='Input IPA file')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Display app information')
    info_parser.add_argument('-i', '--input', required=True, help='Input IPA file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    signer = IPASigner(verbose=args.verbose)
    
    try:
        if args.command == 'resign':
            success = signer.resign_ipa(
                args.input,
                args.certificate,
                args.output,
                args.identity
            )
        elif args.command == 'extract':
            success = signer.extract_ipa(args.input)
        elif args.command == 'verify':
            success = signer.extract_ipa(args.input)
            if success:
                success = signer.verify_signature()
        elif args.command == 'info':
            success = signer.extract_ipa(args.input)
            if success:
                signer.get_app_info()
        
        return 0 if success else 1
    except KeyboardInterrupt:
        signer.log("Operation cancelled", 'WARN')
        return 130
    except Exception as e:
        signer.log(f"Unexpected error: {e}", 'ERROR')
        return 1
    finally:
        signer.cleanup()


if __name__ == '__main__':
    sys.exit(main())
