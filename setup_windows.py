"""
Quick Start Script for Windows Users
Run this script to automatically set up the entire project
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a shell command and report status."""
    print(f"\n{'='*70}")
    print(f"▶ {description}")
    print(f"{'='*70}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(f"Error: {e}")
        return False

def create_directories():
    """Create all necessary project directories."""
    print(f"\n{'='*70}")
    print("▶ Creating project directories")
    print(f"{'='*70}")
    
    directories = [
        'data/raw_frames',
        'data/enhanced_frames',
        'data/labels',
        'data/dataset/images/train',
        'data/dataset/images/val',
        'data/dataset/labels/train',
        'data/dataset/labels/val',
        'data/dataset/crops',
        'models/detector',
        'models/classifier',
        'outputs/annotated_frames',
        'src',
        '.vscode'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")
    
    print("✓ All directories created")

def verify_python():
    """Verify Python installation."""
    print(f"\n{'='*70}")
    print("▶ Verifying Python installation")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✓ Python found: {result.stdout.strip()}")
        
        # Check Python version
        version = sys.version_info
        if version.major >= 3 and version.minor >= 10:
            print(f"✓ Python version is compatible (3.{version.minor}+)")
            return True
        else:
            print(f"✗ Python 3.10+ required, but found 3.{version.minor}")
            return False
    except Exception as e:
        print(f"✗ Python not found: {e}")
        return False

def main():
    print("""
    
╔══════════════════════════════════════════════════════════════════════╗
║                  FISH PIPELINE - WINDOWS QUICK SETUP                 ║
║                                                                      ║
║  This script will automatically:                                    ║
║  1. Verify Python installation                                      ║
║  2. Create project directories                                      ║
║  3. Create virtual environment                                      ║
║  4. Install dependencies                                            ║
║  5. Verify all packages installed                                   ║
║                                                                      ║
║  Total time: ~5-10 minutes                                          ║
║  Make sure you have 2GB free disk space                             ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    input("Press Enter to start setup...")
    
    # Step 1: Verify Python
    if not verify_python():
        print("\n✗ Setup failed: Python 3.10+ required")
        print("Download from: https://www.python.org/downloads/")
        sys.exit(1)
    
    # Step 2: Create directories
    create_directories()
    
    # Step 3: Create virtual environment
    if not run_command(
        f"{sys.executable} -m venv venv",
        "Creating virtual environment"
    ):
        print("\n✗ Failed to create virtual environment")
        sys.exit(1)
    
    # Step 4: Activate venv and install packages
    print(f"\n{'='*70}")
    print("▶ Installing dependencies (this may take several minutes)")
    print(f"{'='*70}")
    
    # Upgrade pip
    if os.name == 'nt':  # Windows
        activate_cmd = r"venv\Scripts\activate.bat && "
    else:  # Unix
        activate_cmd = "source venv/bin/activate && "
    
    if not run_command(
        f"{activate_cmd}{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    ):
        print("⚠ pip upgrade had issues, continuing anyway...")
    
    if not run_command(
        f"{activate_cmd}pip install -r requirements.txt",
        "Installing required packages"
    ):
        print("\n✗ Failed to install dependencies")
        sys.exit(1)
    
    # Step 5: Verify installation
    print(f"\n{'='*70}")
    print("▶ Verifying installation")
    print(f"{'='*70}")
    
    test_imports = (
        f"{activate_cmd}"
        f"{sys.executable} -c \"import cv2, torch, ultralytics, timm; print('✓ All core packages imported successfully')\""
    )
    
    if not run_command(test_imports, "Testing package imports"):
        print("\n⚠ Some packages may not have installed correctly")
    
    # Success message
    print(f"\n{'='*70}")
    print("✓ SETUP COMPLETE!")
    print(f"{'='*70}")
    print("""
    
Next steps:
    1. Place raw underwater frames in: data/raw_frames/
    2. Open VS Code: code .
    3. In VS Code terminal, activate venv:
       - PowerShell: .\\venv\\Scripts\\Activate.ps1
       - Command Prompt: venv\\Scripts\\activate.bat
    4. Run: python src/enhance.py --input data/raw_frames --output data/enhanced_frames
    5. Label frames using Roboflow or CVAT
    6. Continue with remaining stages

For detailed instructions, see: README.md
For Windows-specific help, see: WINDOWS_SETUP.md

Happy fish detecting! 🐠
    """)

if __name__ == '__main__':
    main()
