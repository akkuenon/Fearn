#!/usr/bin/env python3
"""
Fearn IPA Signer - Command-line interface wrapper
"""

import sys
import subprocess
from pathlib import Path

def print_help():
    """Print help message"""
    print("""
Fearn IPA Signer Suite
======================

Available Tools:

1. fearn-signer      - Sign and manage individual IPA files
2. fearn-certmgr     - Manage certificates and provisioning profiles
3. fearn-batch       - Batch sign multiple IPA files
4. fearn-validate    - Validate IPA structure and integrity

Usage:
  fearn <tool> [options]

Examples:
  fearn fearn-signer resign -i app.ipa -c "iPhone Developer" -o signed.ipa
  fearn fearn-certmgr list-certs
  fearn fearn-batch -i ./ipa_files -c "iPhone Developer" -o ./signed
  fearn fearn-validate -i app.ipa

For detailed help on each tool:
  python3 fearn_signer.py --help
  python3 fearn_cert_manager.py --help
  python3 fearn_batch_signer.py --help
  python3 fearn_validator.py --help
    """)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    tool = sys.argv[1]
    args = sys.argv[2:]
    
    script_map = {
        'fearn-signer': 'fearn_signer.py',
        'fearn-certmgr': 'fearn_cert_manager.py',
        'fearn-batch': 'fearn_batch_signer.py',
        'fearn-validate': 'fearn_validator.py'
    }
    
    if tool not in script_map:
        print(f"Unknown tool: {tool}")
        print_help()
        sys.exit(1)
    
    script = script_map[tool]
    script_path = Path(__file__).parent / script
    
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        sys.exit(1)
    
    try:
        result = subprocess.run([sys.executable, str(script_path)] + args)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
