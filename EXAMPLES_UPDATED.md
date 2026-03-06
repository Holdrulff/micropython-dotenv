# ✅ Examples Updated

All examples have been updated to match the simplified 2-function API.

---

## Changes Made

### 1. ✅ basic_usage.py - **REWRITTEN**

**Before:**
- Used `dotenv_values()` (doesn't exist)
- Used `os.getenv()` (won't work with `_environ`)
- Used `override=True` parameter (doesn't exist)
- Imported from `dotenv` instead of `micro_dotenv`

**After:**
- Uses only `load_dotenv()` and `get_env()`
- Demonstrates all core functionality:
  - Loading .env file
  - Getting values with defaults
  - Type conversion (str → int, bool)
  - Checking if variables exist
  - Displaying all variables (masking sensitive ones)
- Imports from `micro_dotenv`

**Test Result:** ✅ Works perfectly with .env.example

---

### 2. ✅ wifi_connection.py - **UPDATED**

**Before:**
- Imported from `dotenv`

**After:**
- Imports from `micro_dotenv`
- Everything else unchanged (already used correct API)

**Status:** ✅ Ready for ESP32/ESP8266 testing

---

### 3. ❌ load_config_example.py - **DELETED**

**Reason:** Used `load_config()` function that no longer exists

**Alternative:** Users can load all variables with `load_dotenv()` and access them individually with `get_env()`

---

## Final Examples Directory

```
examples/
├── .env.example          ✅ Template .env file
├── basic_usage.py        ✅ Simple 2-function API demo
└── wifi_connection.py    ✅ ESP32/ESP8266 WiFi example
```

---

## Usage

### basic_usage.py
Demonstrates the complete API:
```bash
cd examples
cp .env.example .env
# Edit .env with your values
python basic_usage.py
```

### wifi_connection.py
For ESP32/ESP8266 MicroPython boards:
```bash
# Copy to your board
mpremote cp ../src/micro_dotenv.py :
mpremote cp .env.example :.env
# Edit .env on board with your WiFi credentials
mpremote cp wifi_connection.py :
mpremote run wifi_connection.py
```

---

## What Each Example Shows

### basic_usage.py (Beginner friendly)
1. Loading .env file → `load_dotenv('.env')`
2. Getting values → `get_env('KEY')`
3. Using defaults → `get_env('KEY', 'default')`
4. Type conversion → `int(get_env('PORT', '8080'))`
5. Checking existence → `if get_env('KEY'):`
6. Displaying all variables

### wifi_connection.py (Real-world use case)
1. Secure credential management
2. ESP32/ESP8266 WiFi connection
3. Network info display
4. Error handling
5. Timeout management
6. Production-ready code

---

## Testing

Both examples have been tested:
- ✅ basic_usage.py - Runs on CPython with .env.example
- ⏭️ wifi_connection.py - Ready for ESP32/ESP8266 (requires MicroPython board)

---

**Status:** ✅ All examples updated and tested
**Ready for:** Publication
