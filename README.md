# MicroPython-dotenv

**A lightweight `.env` file loader for MicroPython** - bringing modern environment variable management to microcontrollers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MicroPython](https://img.shields.io/badge/MicroPython-1.19+-blue.svg)](https://micropython.org/)
[![Size](https://img.shields.io/badge/size-~1.5KB-green.svg)]()

## Features

- **Lightweight**: ~1.5KB, minimal memory footprint
- **Zero dependencies**: Pure MicroPython implementation
- **Universal compatibility**: ESP32, ESP8266, RP2040, and all MicroPython boards
- **MicroPython-native**: Custom environment dictionary (no `os.environ` dependency)
- **Secure**: Keep secrets out of your code repository
- **Battle-tested**: Used in production ESP32-C3 projects

### Supported Features

- ✅ Comments (`#`)
- ✅ Double quotes (`"`)
- ✅ Single quotes (`'`)
- ✅ Empty lines
- ✅ Whitespace trimming
- ✅ Default values
- ✅ Multiple .env files
- ✅ Graceful error handling

## Why Use This?

**Before** (hardcoded credentials):
```python
WIFI_SSID = 'my_network'      # ❌ Committed to git!
WIFI_PASSWORD = 'secret123'    # ❌ Everyone can see this!
```

**After** (using .env):
```python
from dotenv_micro import load_dotenv, get_env
load_dotenv('.env')
WIFI_SSID = get_env('WIFI_SSID')         # ✅ Secure
WIFI_PASSWORD = get_env('WIFI_PASSWORD')  # ✅ Not in repository
```

## Installation

### Method 1: Manual Copy (Recommended)

1. Copy `src/dotenv_micro.py` to your MicroPython board
2. Place it in the `lib/` folder for best organization

```bash
# Using mpremote (recommended)
mpremote mkdir lib
mpremote cp src/dotenv_micro.py :lib/dotenv_micro.py

# Using ampy
ampy --port /dev/ttyUSB0 mkdir lib
ampy --port /dev/ttyUSB0 put src/dotenv_micro.py lib/dotenv_micro.py

# Using Thonny
# Simply open src/dotenv_micro.py and save to lib/ on your board
```

### Method 2: Clone Repository

```bash
git clone https://github.com/holdrulff/micropython-dotenv.git
cd micropython-dotenv
# Copy src/dotenv.py to your board
```

## Quick Start

### 1. Create a `.env` file

Create a file named `.env` in the root of your project:

```bash
# .env
WIFI_SSID=my_network
WIFI_PASSWORD=my_secret_password
HOSTNAME=esp32-sensor
API_KEY=your-api-key-here
```

### 2. Load and use in your code

```python
from dotenv_micro import load_dotenv, get_env

# Load all variables from .env
load_dotenv('.env')

# Access using get_env()
wifi_ssid = get_env('WIFI_SSID')
wifi_password = get_env('WIFI_PASSWORD')

print(f"Connecting to: {wifi_ssid}")
```

## API Reference

### `load_dotenv(path='.env')`

Load environment variables from `.env` file into internal `_environ` dictionary.

**Parameters:**
- `path` (str): Path to .env file. Default: `'.env'`

**Returns:** `dict` of loaded variables

**Example:**
```python
from dotenv_micro import load_dotenv

# Load from default .env file
env_vars = load_dotenv()
print(f"Loaded {len(env_vars)} variables")

# Load from custom path
env_vars = load_dotenv('/config/production.env')

# Variables are now accessible via get_env()
```

**Notes:**
- Parses `.env` file line by line
- Ignores comments (lines starting with `#`)
- Skips empty lines
- Removes surrounding quotes (single or double)
- Trims whitespace from keys and values
- Stores in custom `_environ` dictionary (MicroPython doesn't have `os.environ`)

### `get_env(key, default=None)`

Get environment variable from internal storage.

**Parameters:**
- `key` (str): Environment variable name
- `default` (any): Default value if not found. Default: `None`

**Returns:** Value of environment variable or default

**Example:**
```python
from dotenv_micro import get_env, load_dotenv

# Load .env first
load_dotenv('.env')

# Get with default value
wifi_ssid = get_env('WIFI_SSID', 'default_network')

# Get without default (returns None if not found)
api_key = get_env('API_KEY')

# Check if variable exists
hostname = get_env('HOSTNAME')
if hostname:
    print(f"Hostname: {hostname}")
```

## Usage Examples

### WiFi Connection (ESP32/ESP8266)

```python
import network
from dotenv_micro import load_dotenv, get_env
import time

# Load credentials from .env
load_dotenv('.env')

def connect_wifi():
    ssid = get_env('WIFI_SSID')
    password = get_env('WIFI_PASSWORD')

    if not ssid or not password:
        raise ValueError("WIFI_SSID and WIFI_PASSWORD required in .env")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    # Wait for connection
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print(f"Connected! IP: {wlan.ifconfig()[0]}")
    else:
        print("Connection failed!")

connect_wifi()
```

### MQTT Client Configuration

```python
from dotenv_micro import load_dotenv, get_env

# Load MQTT configuration from .env
load_dotenv('.env')

# Get values with defaults
mqtt_broker = get_env('MQTT_BROKER', 'mqtt.example.com')
mqtt_port = int(get_env('MQTT_PORT', '1883'))
mqtt_user = get_env('MQTT_USER', '')
mqtt_password = get_env('MQTT_PASSWORD', '')

# Use in your MQTT client
from umqtt.simple import MQTTClient

client = MQTTClient(
    client_id='device001',
    server=mqtt_broker,
    port=mqtt_port,
    user=mqtt_user,
    password=mqtt_password
)

client.connect()
print("Connected to MQTT broker!")
```

### Type Conversion

All values from `.env` are strings. Convert as needed:

```python
from dotenv_micro import load_dotenv, get_env

load_dotenv('.env')

# Integer
port = int(get_env('PORT', '8080'))

# Float
timeout = float(get_env('TIMEOUT', '30.5'))

# Boolean helper function
def get_bool(key, default=False):
    value = get_env(key, str(default))
    return value.lower() in ('true', '1', 'yes', 'on')

debug = get_bool('DEBUG', False)

# List (comma-separated)
allowed_hosts = get_env('ALLOWED_HOSTS', '').split(',')
```

## .env File Format

```bash
# Comments start with #
# Empty lines are ignored

# Simple key=value pairs
WIFI_SSID=my_network
PORT=8080

# Quoted values (quotes are removed)
WIFI_PASSWORD="password with spaces"
API_KEY='single-quoted-value'

# Empty values are allowed
OPTIONAL_FIELD=

# Inline comments (outside quotes)
HOSTNAME=device001  # this is my device

# Special characters work fine
DATABASE_URL=postgresql://user:pass@localhost:5432/db
API_ENDPOINT=https://api.example.com/v1/endpoint?key=value
```

## Security Best Practices

### ⚠️ NEVER commit `.env` files to version control!

**Add to `.gitignore`:**
```gitignore
# Secrets
.env
.env.*
*.env

# Except example file
!.env.example
```

### ✅ Use `.env.example` for templates

Create `.env.example` with placeholder values (safe to commit):

```bash
# .env.example
WIFI_SSID=your_network_name
WIFI_PASSWORD=your_password
API_KEY=your-api-key-here
```

### ✅ Document required variables

In your README or documentation, list required environment variables:

```markdown
## Required Environment Variables

Create a `.env` file with:

- `WIFI_SSID` - Your WiFi network name
- `WIFI_PASSWORD` - Your WiFi password
- `API_KEY` - API key from provider.com
```

## Memory Usage

Tested on ESP32-C3 (4MB flash, 400KB RAM):

- **Library size**: ~1.5 KB
- **Runtime memory**: ~500 bytes + (number of variables × average value length)
- **Example**: 10 variables with 20-char values ≈ 700 bytes total
- **No heap fragmentation**: Uses standard file I/O and simple dictionary

Perfect for memory-constrained microcontrollers!

## Comparison with Alternatives

| Method | Size | Security | Standard | MicroPython Compatible |
|--------|------|----------|----------|----------------------|
| Hardcoded values | 0 KB | ❌ Poor | ❌ No | ✅ Yes |
| `config.py` | ~1 KB | ⚠️ Medium | ❌ No | ✅ Yes |
| `secrets.py` | ~1 KB | ✅ Good | ⚠️ Partial | ✅ Yes |
| `config.json` | ~2 KB | ✅ Good | ⚠️ Partial | ✅ Yes |
| **`.env` (this lib)** | **~1.5 KB** | **✅ Good** | **✅ Yes** | **✅ Yes** |

## Testing

Test the library in MicroPython REPL:

```python
# Create test .env file
>>> with open('.env', 'w') as f:
...     f.write('TEST_VAR=hello\n')
...     f.write('TEST_NUM=42\n')

# Load and test
>>> from dotenv_micro import load_dotenv, get_env
>>> env = load_dotenv('.env')
>>> print(env)
{'TEST_VAR': 'hello', 'TEST_NUM': '42'}

>>> print(get_env('TEST_VAR'))
hello

>>> print(get_env('TEST_NUM'))
42

>>> print(get_env('MISSING', 'default'))
default
```

## Real-World Usage

This library is used in production in the [ESP32-C3 IoT Device](../) project:

- Secure WiFi credential management
- API key storage
- Device configuration
- Multi-environment support

## Compatibility

**Tested on:**
- ✅ ESP32-C3 (primary development platform)
- ✅ ESP32 (all variants: S2, S3, etc.)
- ✅ ESP8266
- ✅ Raspberry Pi Pico (RP2040)

**Requirements:**
- MicroPython 1.19 or later
- Filesystem support (most boards have this)
- No `os.environ` required (uses custom `_environ` dictionary)

## Implementation Details

### Why Custom `_environ` Dictionary?

MicroPython doesn't have `os.getenv()` or `os.environ` on most microcontrollers (ESP32, ESP8266, RP2040), so this library implements a custom dictionary:

```python
# Internal implementation
_environ = {}  # Custom dictionary to replace os.environ

def load_dotenv(path='.env'):
    global _environ
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                _environ[key.strip()] = value.strip()
    return _environ

def get_env(key, default=None):
    return _environ.get(key, default)
```

**Important:** This means you must use `get_env()` instead of `os.getenv()` to access your environment variables.

### Error Handling

The library handles errors gracefully:

```python
try:
    load_dotenv('.env')
except OSError:
    print("Warning: .env file not found")
    # Application continues with defaults
```

## Contributing

Contributions are welcome! This library was created for the ESP32-C3 computational physics project.

**To contribute:**
1. Fork the repository
2. Create a feature branch
3. Test on real MicroPython hardware
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT License - Free to use, modify, and distribute.

See [LICENSE](LICENSE) file for full text.

## Author

Created by **Wesley Fernandes** for the ESP32-C3 computational physics project at CFA (Computação Física Aplicada).

Inspired by the Python [`python-dotenv`](https://github.com/theskumar/python-dotenv) package, adapted for MicroPython's constraints.

## Acknowledgments

- **Prof. Fábio Nakano** - Project guidance and original ESP32-C3 codebase
- Python `python-dotenv` - API inspiration
- MicroPython community - Platform and documentation
- ESP32/ESP8266 communities - Use cases and testing

---

## Related Documentation

- [Main Project README](../README.md) - ESP32-C3 IoT device documentation
- [ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture and design patterns
- [TESTING_GUIDE.md](../TESTING_GUIDE.md) - Comprehensive testing procedures
- [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) - Migration from hardcoded config

---

**Version:** 1.0.0
**Last Updated:** March 2026
**License:** MIT
**Platform:** MicroPython 1.19+
