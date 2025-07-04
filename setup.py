#!/usr/bin/env python3
"""
P4CK37 GL0TT0N Setup Script
Automated setup and dependency installation
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - Compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    requirements = [
        "colorama>=0.4.4",
        "requests>=2.28.0", 
        "PySocks>=1.7.1"
    ]
    
    print("\n🔧 Installing dependencies...")
    for req in requirements:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", req], 
                         check=True, capture_output=True)
            print(f"✅ Installed: {req}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install: {req}")
            return False
    return True

def create_directories():
    """Create necessary directories"""
    dirs = ["examples", "docs", "logs"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Created directory: {dir_name}")

def check_main_script():
    """Check if main script exists"""
    if Path("packet_glutton.py").exists():
        print("✅ Main script found: packet_glutton.py")
        return True
    else:
        print("❌ Main script not found: packet_glutton.py")
        print("   Make sure you have the main script in this directory")
        return False

def run_setup():
    """Main setup function"""
    print("🍽️  P4CK37 GL0TT0N Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Check main script
    print("\n🔍 Checking files...")
    if not check_main_script():
        return False
    
    print("\n🎯 Setup Complete!")
    print("\nTo run P4CK37 GL0TT0N:")
    print("  python packet_glutton.py")
    print("\nFor help:")
    print("  cat README.md")
    
    return True

if __name__ == "__main__":
    success = run_setup()
    sys.exit(0 if success else 1)