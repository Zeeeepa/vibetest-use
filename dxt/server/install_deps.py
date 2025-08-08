#!/usr/bin/env python3
"""
Dependency installer for Vibetest DXT
This script installs required Python packages when the DXT is first run
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies using pip"""
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if not os.path.exists(requirements_file):
        print("Requirements file not found!")
        return False
    
    try:
        # Install dependencies
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', 
            '-r', requirements_file,
            '--user',  # Install to user directory to avoid permission issues
            '--quiet'
        ])
        
        # Install playwright browsers
        subprocess.check_call([
            sys.executable, '-m', 'playwright', 'install', 'chromium',
            '--quiet'
        ])
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

if __name__ == "__main__":
    success = install_dependencies()
    sys.exit(0 if success else 1)
