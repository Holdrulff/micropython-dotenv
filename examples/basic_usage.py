"""
Basic usage examples for micropython-dotenv

Demonstrates the simple 2-function API for managing environment variables.
"""

import sys

# Add parent directory to path to import micro_dotenv
sys.path.insert(0, '../src')

from micro_dotenv import load_dotenv, get_env

print("=" * 50)
print("MicroPython-dotenv Basic Usage Examples")
print("=" * 50)

# Example 1: Load all variables
print("\n1. Using load_dotenv() - Load all variables")
print("-" * 50)
env_vars = load_dotenv('.env')
print(f"Loaded {len(env_vars)} variables from .env")

# Example 2: Get specific variables
print("\n2. Using get_env() - Get specific values")
print("-" * 50)
wifi_ssid = get_env('WIFI_SSID')
wifi_password = get_env('WIFI_PASSWORD')
hostname = get_env('HOSTNAME', 'esp32-default')  # with default

print(f"WIFI_SSID: {wifi_ssid}")
print(f"WIFI_PASSWORD: {'*' * 8 if wifi_password else 'Not set'}")
print(f"HOSTNAME: {hostname}")

# Example 3: Get with defaults
print("\n3. Default Values")
print("-" * 50)
device_id = get_env('DEVICE_ID', 'unknown_device')
api_timeout = get_env('API_TIMEOUT', '60')  # Note: all values are strings
debug = get_env('DEBUG', 'false')

print(f"DEVICE_ID: {device_id}")
print(f"API_TIMEOUT: {api_timeout}")
print(f"DEBUG: {debug}")

# Example 4: Type conversion (all values are strings)
print("\n4. Type Conversion")
print("-" * 50)
timeout_str = get_env('API_TIMEOUT', '30')
timeout_int = int(timeout_str)
print(f"Timeout as string: '{timeout_str}' (type: {type(timeout_str).__name__})")
print(f"Timeout as int: {timeout_int} (type: {type(timeout_int).__name__})")

debug_str = get_env('DEBUG', 'false')
debug_bool = debug_str.lower() in ('true', '1', 'yes')
print(f"Debug as string: '{debug_str}'")
print(f"Debug as bool: {debug_bool}")

# Example 5: Check if variable exists
print("\n5. Checking if Variables Exist")
print("-" * 50)
api_key = get_env('API_KEY')
if api_key:
    print(f"API_KEY is set: {'*' * 8}")
else:
    print("API_KEY is not set")

optional_value = get_env('OPTIONAL_VALUE')
if optional_value is None:
    print("OPTIONAL_VALUE is not set (None)")
else:
    print(f"OPTIONAL_VALUE: {optional_value}")

# Example 6: Display all loaded variables
print("\n6. All Loaded Variables")
print("-" * 50)
print(f"Total variables loaded: {len(env_vars)}")
for key, value in env_vars.items():
    # Mask sensitive values for display
    if 'PASSWORD' in key or 'KEY' in key or 'SECRET' in key:
        display_value = '*' * 8
    else:
        display_value = value
    print(f"  {key}: {display_value}")

print("\n" + "=" * 50)
print("Examples completed!")
print("=" * 50)
