# Contributing to MicroPython-dotenv

Thank you for your interest in contributing! This library was created for the MicroPython community, and contributions are welcome.

## Code of Conduct

Please be respectful and inclusive. Welcome newcomers, focus on constructive feedback, and remember: we're all volunteers.

## Getting Started

Before contributing, please:

1. Read this guide completely
2. Run the setup script: `python setup_dev_env.py`
3. Familiarize yourself with the codebase
4. Check existing [Issues](https://github.com/holdrulff/micropython-dotenv/issues) and [Pull Requests](https://github.com/holdrulff/micropython-dotenv/pulls)

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check if it's already reported in [Issues](https://github.com/holdrulff/micropython-dotenv/issues)
2. If not, open a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - MicroPython version and board type (e.g., "ESP32-C3, MicroPython v1.20")
   - Minimal code example
   - Contents of your .env file (with sensitive data removed)

### Suggesting Features

We welcome feature suggestions! Please:

1. Check [Issues](https://github.com/holdrulff/micropython-dotenv/issues) first
2. Open a new issue with:
   - Clear description of the feature
   - Use case / why it's useful
   - Example of how it would be used
   - Consider memory/performance impact (this is for microcontrollers!)

### Pull Requests

**Before submitting:**

1. Discuss major changes in an issue first
2. Keep changes focused and atomic
3. Follow the code style (see below)
4. Add tests for new features
5. Update documentation
6. Test on real hardware if possible
7. **Sign off your commits** (see below)

**Process:**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `python tests/test_dotenv.py`
5. Format code: `ruff format src/` (optional but recommended)
6. Commit with clear messages and sign-off: `git commit -s`
7. Push and create a pull request

## Commit Guidelines

Following MicroPython conventions, each commit message must:

### 1. Use a file/directory prefix

Start with the file or directory affected:

```
src/dotenv: Add support for multiline values.
tests: Fix test_override_mode for _environ.
README: Update installation instructions.
examples: Add MQTT configuration example.
```

### 2. Write a clear, grammatical first line

- Keep it under 72 characters
- End with a period
- Describe what the change does, not how

**Good examples:**
```
src/dotenv: Add dotenv_values() function for reading without setting env.
src/dotenv_micro: Fix quote handling in values.
tests: Add tests for special characters in values.
```

**Bad examples:**
```
fix bug
Updated code
WIP
```

### 3. Add detailed description if needed

After the first line, add an empty line and detailed description for complex changes:

```
src/dotenv: Add support for multiline values.

This change allows values to span multiple lines when enclosed in quotes.
The implementation uses a state machine to track quote boundaries and
only adds ~50 bytes to the compiled size.

Fixes #42
```

### 4. Sign off your commits

**YOU MUST sign off every commit** by adding a "Signed-off-by:" line. Use `git commit -s`:

```bash
git commit -s -m "src/dotenv: Add multiline value support."
```

This adds:
```
Signed-off-by: Your Name <holdrulff@gmail.com>
```

**By signing off, you certify that:**

- You wrote the change yourself, or took it from a compatible open-source project
- You are allowed to release these changes to an open-source project
- You agree to release the changes under the MIT license
- Your contribution will be publicly available indefinitely
- Your signature includes your full real name and active email address

**This is required for all contributions.**

## Code Style

### General Guidelines

- **Keep it simple**: This is for microcontrollers with limited resources
- **No external dependencies**: Only MicroPython stdlib
- **Memory efficient**: Avoid creating unnecessary objects
- **Well documented**: Docstrings for all public functions
- **Tested**: Add tests for new features

### Python Style

Follow PEP 8 with these considerations:

- Line length: 99 characters maximum
- Use 4 spaces for indentation (no tabs)
- Use `snake_case` for functions and variables
- Use `CAPS_WITH_UNDERSCORE` for constants
- Format with `ruff format` (optional but recommended)

```python
# Good: Simple, memory efficient
def parse_value(value):
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    return value

# Bad: Complex, creates unnecessary objects
def parse_value(value):
    import re
    matches = re.findall(r'^"(.*)"$', value)
    return matches[0] if matches else value
```

### Docstring Format

Use Google-style docstrings:

```python
def my_function(arg1, arg2='default'):
    """
    Brief description of function.

    Longer description if needed. Explain what it does,
    not how it does it.

    Args:
        arg1 (str): Description of arg1
        arg2 (str): Description of arg2. Default: 'default'

    Returns:
        dict: Description of return value

    Raises:
        ValueError: When this error occurs

    Example:
        >>> result = my_function('test')
        >>> print(result)
    """
    pass
```

## Testing

### Running Tests

**On CPython:**
```bash
cd tests
python test_dotenv.py
```

**On MicroPython board:**
```bash
mpremote cp tests/test_dotenv.py :
mpremote exec "import test_dotenv; test_dotenv.run_all_tests()"
```

### Writing Tests

Add tests for new features in `tests/test_dotenv.py`:

```python
def test_my_feature(runner):
    """Test description"""
    # Setup
    create_test_env('.env.test', 'KEY=value')

    # Test
    result = my_function()

    # Assert
    runner.assert_equal(result, expected)

    # Cleanup
    cleanup_test_env()
```

### Test Guidelines

- Test happy path and edge cases
- Test error handling
- Clean up test files (use `cleanup_test_env()`)
- Keep tests fast (this runs on microcontrollers!)
- One test per function/feature

## Documentation

### Update README

When adding features, update:

- API Reference section
- Usage Examples
- Feature list

### Update CHANGELOG

Add entry to `CHANGELOG.md`:

```markdown
## [Unreleased]

### Added
- New feature description (#PR_NUMBER)

### Fixed
- Bug fix description (#ISSUE_NUMBER)

### Changed
- Breaking change description
```

### Code Comments

- Comment **why**, not **what**
- Explain non-obvious decisions
- Reference issue numbers when relevant

```python
# Good: Explains why
# We check _environ first for performance (avoid file I/O)
if key in _environ:
    return _environ[key]

# Bad: States the obvious
# Get key from _environ
if key in _environ:
    return _environ[key]
```

## Hardware Testing

If possible, test on real hardware:

- ESP32 (various models: C3, S2, S3)
- ESP8266
- Raspberry Pi Pico (RP2040)
- Other MicroPython boards

Report compatibility in your PR:
```
Tested on:
- ✅ ESP32-C3 (MicroPython v1.20)
- ✅ RP2040 (MicroPython v1.19)
- ⏭️ ESP8266 (not available)
```

## Memory Considerations

This library runs on microcontrollers with limited resources:

### Memory Budget
- Keep library size under 2KB
- Minimize RAM usage
- Avoid heap fragmentation

### Good Practices
```python
# Good: In-place operations
value = value.strip()

# Bad: Creates intermediate strings
value = value.lstrip().rstrip()

# Good: Generator
for line in file:
    process(line)

# Bad: Loads all into memory
lines = file.readlines()
for line in lines:
    process(line)
```

## Performance

- File I/O is expensive on microcontrollers
- Cache results when possible
- Avoid repeated file reads

```python
# Good: Load once at startup
load_dotenv()
wifi_ssid = get_env('WIFI_SSID')

# Bad: Re-read file every time
def get_value(key):
    return load_dotenv().get(key)  # Don't do this!
```

## Development Workflow

### 1. Setup

```bash
# Clone repository
git clone https://github.com/holdrulff/micropython-dotenv.git
cd micropython-dotenv

# Run setup script
python setup_dev_env.py

# Create test .env
cp examples/.env.example .env
```

### 2. Make Changes

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes to src/dotenv.py
# Add tests to tests/test_dotenv.py
# Update documentation
```

### 3. Test

```bash
# Run tests on CPython
python tests/test_dotenv.py

# Format code (optional)
ruff format src/

# Test on MicroPython board
mpremote cp src/dotenv.py :
mpremote exec "import dotenv; print(dotenv.__version__)"
```

### 4. Commit

```bash
# Commit with sign-off
git add src/dotenv.py tests/test_dotenv.py
git commit -s -m "src/dotenv: Add my new feature.

This feature adds support for X because Y.
Implementation uses Z approach to minimize memory usage."

# Push
git push origin feature/my-feature
```

### 5. Create Pull Request

- Fill out the PR template completely
- Explain what changed and why
- Reference related issues
- List testing performed
- Note any breaking changes

## Questions?

- Open a [Discussion](https://github.com/holdrulff/micropython-dotenv/discussions)
- Ask in [MicroPython forums](https://forum.micropython.org/)
- Check existing [Issues](https://github.com/holdrulff/micropython-dotenv/issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MicroPython-dotenv!

Signed-off-by: Wesley Fernandes <holdrulff@gmail.com>
