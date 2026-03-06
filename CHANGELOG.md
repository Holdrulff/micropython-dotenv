# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-06

### Added
- Initial release
- Core functions: `load_dotenv()`, `get_env()`, `dotenv_values()`
- Helper function: `load_config()` for loading multiple variables
- Support for comments (#)
- Support for single and double quotes
- Support for inline comments
- Support for empty values
- Comprehensive test suite
- Examples for WiFi, MQTT, and basic usage
- Complete documentation

### Features
- Lightweight (~1KB)
- Zero dependencies
- Compatible with ESP32, ESP8266, RP2040
- Memory efficient
- Encoding support (UTF-8)
- Override mode
- Type conversion examples

### Documentation
- Complete README with examples
- API reference
- Security best practices
- Migration guide from hardcoded values
- Comparison with alternatives

## [Unreleased]

### Planned Features
- Variable expansion (`${VAR}` syntax)
- Multi-line value support
- `.env.local` override files
- Validation helpers
- Better error messages with line numbers

### Ideas
- Integration with popular MicroPython frameworks
- Configuration file format auto-detection (JSON, TOML)
- Encrypted .env file support
- Web-based configuration interface

---

## Version History

- **v1.0.0** (2026-03-06) - Initial public release
