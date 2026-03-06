#!/usr/bin/env python3
"""
Developer environment setup helper for micropython-dotenv

This script helps developers quickly set up their environment for
contributing to micropython-dotenv.
"""

import os
import sys


def create_env_example():
    """Create .env.example template if it doesn't exist."""
    env_example_path = 'examples/.env.example'
    if os.path.exists(env_example_path):
        print(f"✓ {env_example_path} already exists")
        return

    content = """# Example .env configuration for micropython-dotenv
# Copy this file to .env and fill in your actual values

# WiFi credentials
WIFI_SSID=your_network_name
WIFI_PASSWORD=your_password

# Device configuration
HOSTNAME=esp32-device
DEBUG=false

# API configuration
API_KEY=your-api-key-here
API_ENDPOINT=https://api.example.com

# MQTT configuration (optional)
MQTT_BROKER=mqtt.example.com
MQTT_PORT=1883
MQTT_USER=
MQTT_PASSWORD=
"""
    os.makedirs('examples', exist_ok=True)
    with open(env_example_path, 'w') as f:
        f.write(content)
    print(f"✓ Created {env_example_path}")


def create_gitignore():
    """Ensure .gitignore protects .env files."""
    gitignore_path = '.gitignore'
    required_entries = [
        '# Environment variables',
        '.env',
        '.env.*',
        '*.env',
        '',
        '# Except example files',
        '!.env.example',
        '!examples/.env.example',
        '',
        '# Python',
        '__pycache__/',
        '*.py[cod]',
        '*$py.class',
        '*.so',
        '.Python',
        '',
        '# Testing',
        '.env.test',
        'test_*.env',
        '',
        '# IDE',
        '.vscode/',
        '.idea/',
        '*.swp',
        '*.swo',
        '*~',
        '',
        '# OS',
        '.DS_Store',
        'Thumbs.db',
    ]

    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            existing = f.read()
        if '.env' in existing:
            print(f"✓ {gitignore_path} already configured")
            return

    with open(gitignore_path, 'a') as f:
        f.write('\n'.join(required_entries) + '\n')
    print(f"✓ Updated {gitignore_path}")


def create_test_env():
    """Create a test .env file for development."""
    test_env_path = '.env.test'
    if os.path.exists(test_env_path):
        print(f"✓ {test_env_path} already exists")
        return

    content = """# Test environment configuration
TEST_VAR=test_value
QUOTED_VAR="quoted value"
SINGLE_QUOTED='single quoted'
NUMBER=42
EMPTY_VALUE=
"""
    with open(test_env_path, 'w') as f:
        f.write(content)
    print(f"✓ Created {test_env_path} for testing")


def check_dependencies():
    """Check if required development tools are available."""
    print("\nChecking development dependencies:")

    # Check Python version
    if sys.version_info < (3, 6):
        print("✗ Python 3.6+ required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")

    # Check for ruff (optional but recommended)
    try:
        import subprocess
        result = subprocess.run(['ruff', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ ruff installed")
        else:
            print("⚠ ruff not found (optional, for code formatting)")
    except FileNotFoundError:
        print("⚠ ruff not found (optional, install with: pip install ruff)")

    return True


def print_next_steps():
    """Print next steps for the developer."""
    print("\n" + "="*60)
    print("Development environment setup complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Copy examples/.env.example to .env and fill in your values")
    print("  2. Run tests: python tests/test_dotenv.py")
    print("  3. Test on MicroPython board:")
    print("     mpremote cp src/dotenv.py :")
    print("     mpremote exec 'import dotenv; print(dotenv.__version__)'")
    print("\nFor code formatting (optional):")
    print("  ruff format src/")
    print("\nFor contributing:")
    print("  - Read CONTRIBUTING.md")
    print("  - Follow MicroPython code conventions")
    print("  - Sign-off commits with: git commit -s")
    print("\n" + "="*60)


def main():
    """Main setup function."""
    print("="*60)
    print("MicroPython-dotenv Development Environment Setup")
    print("="*60)
    print()

    try:
        create_env_example()
        create_gitignore()
        create_test_env()
        check_dependencies()
        print_next_steps()
        return 0
    except Exception as e:
        print(f"\n✗ Error during setup: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
