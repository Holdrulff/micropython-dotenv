"""
WiFi Connection Example using micropython-dotenv

Demonstrates secure WiFi credential management on ESP32/ESP8266.
Works with ESP32, ESP32-C3, ESP32-S2, ESP32-S3, ESP8266, etc.
"""

import sys
import time

# Add parent directory to path to import dotenv
sys.path.insert(0, '../src')

from micro_dotenv import load_dotenv, get_env

# Import network module (works on ESP32 and ESP8266)
try:
    import network
except ImportError:
    print("ERROR: network module not available (not running on MicroPython device?)")
    sys.exit(1)


def connect_wifi(ssid=None, password=None, hostname=None, timeout=30):
    """
    Connect to WiFi using credentials from .env file.

    Args:
        ssid (str): WiFi SSID (loaded from .env if not provided)
        password (str): WiFi password (loaded from .env if not provided)
        hostname (str): Device hostname (loaded from .env if not provided)
        timeout (int): Connection timeout in seconds

    Returns:
        bool: True if connected, False otherwise
    """
    # Load credentials from .env if not provided
    if ssid is None:
        ssid = get_env('WIFI_SSID')
    if password is None:
        password = get_env('WIFI_PASSWORD')
    if hostname is None:
        hostname = get_env('HOSTNAME', 'micropython-device')

    # Validate credentials
    if not ssid or not password:
        print("ERROR: WIFI_SSID and WIFI_PASSWORD must be set in .env file")
        print("Create a .env file with:")
        print("  WIFI_SSID=your_network")
        print("  WIFI_PASSWORD=your_password")
        return False

    print(f"Connecting to WiFi: {ssid}")
    print(f"Hostname: {hostname}")

    # Initialize WiFi in station mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Set hostname if supported (ESP32)
    try:
        wlan.config(dhcp_hostname=hostname)
    except:
        pass  # Not all boards support hostname configuration

    # Check if already connected
    if wlan.isconnected():
        print(f"Already connected!")
        print_network_info(wlan)
        return True

    # Connect to network
    wlan.connect(ssid, password)

    # Wait for connection
    start_time = time.time()
    while not wlan.isconnected():
        if time.time() - start_time > timeout:
            print(f"ERROR: Connection timeout after {timeout} seconds")
            return False

        print(".", end="")
        time.sleep(0.5)

    print("\nConnected successfully!")
    print_network_info(wlan)
    return True


def print_network_info(wlan):
    """
    Print network configuration information.

    Args:
        wlan: WLAN object
    """
    if not wlan.isconnected():
        print("Not connected to WiFi")
        return

    ifconfig = wlan.ifconfig()
    print("\nNetwork Configuration:")
    print(f"  IP Address:  {ifconfig[0]}")
    print(f"  Subnet Mask: {ifconfig[1]}")
    print(f"  Gateway:     {ifconfig[2]}")
    print(f"  DNS Server:  {ifconfig[3]}")

    # Get signal strength (RSSI) if available
    try:
        rssi = wlan.status('rssi')
        print(f"  Signal (RSSI): {rssi} dBm")
    except:
        pass


def disconnect_wifi():
    """Disconnect from WiFi and disable interface."""
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        print("Disconnected from WiFi")
    wlan.active(False)
    print("WiFi interface disabled")


# Main execution
if __name__ == '__main__':
    print("=" * 50)
    print("WiFi Connection Example with micropython-dotenv")
    print("=" * 50)

    # Load .env file
    print("\nLoading .env file...")
    env_vars = load_dotenv('.env')

    if not env_vars:
        print("WARNING: No .env file found or file is empty")
        print("Please create .env file with your WiFi credentials")
    else:
        print(f"Loaded {len(env_vars)} configuration variables")

    # Connect to WiFi
    print("\n" + "-" * 50)
    if connect_wifi():
        print("\nWiFi connection successful!")

        # Keep connection alive for 10 seconds
        print("\nKeeping connection alive for 10 seconds...")
        time.sleep(10)

        # Disconnect
        print("\n" + "-" * 50)
        disconnect_wifi()
    else:
        print("\nFailed to connect to WiFi")

    print("\n" + "=" * 50)
    print("Example completed")
    print("=" * 50)
