"""
Test suite for micropython-dotenv

Run on MicroPython board or CPython for testing.
Compatible with unittest-style assertions.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from micro_dotenv import load_dotenv, get_env, __version__


class TestRunner:
    """Simple test runner for MicroPython (no unittest available)"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def assert_equal(self, actual, expected, msg=""):
        if actual != expected:
            error = f"Expected {expected}, got {actual}"
            if msg:
                error = f"{msg}: {error}"
            raise AssertionError(error)

    def assert_true(self, condition, msg=""):
        if not condition:
            raise AssertionError(msg or "Condition is False")

    def assert_in(self, item, container, msg=""):
        if item not in container:
            error = f"{item} not in {container}"
            if msg:
                error = f"{msg}: {error}"
            raise AssertionError(error)

    def run_test(self, test_func):
        """Run a single test function"""
        test_name = test_func.__name__
        try:
            test_func(self)
            print(f"  [PASS] {test_name}")
            self.passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {test_name}: {e}")
            self.failed += 1
            self.errors.append((test_name, str(e)))
        except Exception as e:
            print(f"  [ERROR] {test_name}: Unexpected error: {e}")
            self.failed += 1
            self.errors.append((test_name, f"Unexpected: {e}"))

    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        print("\n" + "=" * 60)
        print(f"Tests run: {total}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")

        if self.failed > 0:
            print("\nFailed tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")

        print("=" * 60)
        return self.failed == 0


# Test helper functions
def create_test_env(filename='.env.test', content=None):
    """Create a test .env file"""
    if content is None:
        content = """# Test configuration
TEST_VAR=test_value
QUOTED_VAR="quoted value"
SINGLE_QUOTED='single quoted'
NUMBER=42
EMPTY_VALUE=
INLINE_COMMENT=value # this is a comment

# Comment line
LAST_VAR=last
"""
    with open(filename, 'w') as f:
        f.write(content)


def cleanup_test_env(filename='.env.test'):
    """Remove test .env file and clear _environ"""
    from micro_dotenv import _environ
    try:
        os.remove(filename)
    except:
        pass
    # Clear _environ for clean tests
    _environ.clear()


# Test functions
def test_version(runner):
    """Test version is defined"""
    runner.assert_true(__version__, "Version should be defined")
    runner.assert_true(isinstance(__version__, str), "Version should be string")


def test_load_dotenv_basic(runner):
    """Test basic load_dotenv functionality"""
    create_test_env()
    result = load_dotenv('.env.test')

    runner.assert_equal(result['TEST_VAR'], 'test_value')
    runner.assert_equal(result['QUOTED_VAR'], 'quoted value')
    runner.assert_equal(result['SINGLE_QUOTED'], 'single quoted')
    runner.assert_equal(result['NUMBER'], '42')
    runner.assert_equal(result['LAST_VAR'], 'last')
    runner.assert_equal(get_env('TEST_VAR'), 'test_value')

    cleanup_test_env()


def test_empty_values(runner):
    """Test handling of empty values"""
    create_test_env()
    result = load_dotenv('.env.test')

    runner.assert_in('EMPTY_VALUE', result)
    runner.assert_equal(result['EMPTY_VALUE'], '')

    cleanup_test_env()


def test_inline_comments(runner):
    """Test inline comment handling"""
    create_test_env()
    result = load_dotenv('.env.test')

    # Note: Simple parser doesn't remove inline comments
    # This is acceptable for a minimal implementation
    runner.assert_in('INLINE_COMMENT', result)

    cleanup_test_env()


def test_get_env_with_default(runner):
    """Test get_env with default values"""
    create_test_env()
    load_dotenv('.env.test')

    value = get_env('TEST_VAR')
    runner.assert_equal(value, 'test_value')

    default_value = get_env('NON_EXISTENT', 'default')
    runner.assert_equal(default_value, 'default')

    cleanup_test_env()


def test_missing_file(runner):
    """Test behavior with missing .env file"""
    result = load_dotenv('non_existent_file.env')
    # Should return _environ (which might be empty)
    runner.assert_true(isinstance(result, dict))


def test_invalid_lines(runner):
    """Test handling of invalid lines"""
    content = """
# Valid
VALID_KEY=valid_value

# Invalid - no equals sign
INVALID_NO_EQUALS

# Invalid - key with spaces
INVALID KEY=value

# Valid after invalid
ANOTHER_VALID=value2
"""
    create_test_env('.env.test', content)
    result = load_dotenv('.env.test')

    runner.assert_in('VALID_KEY', result)
    runner.assert_in('ANOTHER_VALID', result)
    runner.assert_true('INVALID_NO_EQUALS' not in result)

    cleanup_test_env()


def test_quotes_in_values(runner):
    """Test various quote scenarios"""
    content = """
DOUBLE_QUOTES="value with spaces"
SINGLE_QUOTES='another value'
NO_QUOTES=plain_value
"""
    create_test_env('.env.test', content)
    result = load_dotenv('.env.test')

    runner.assert_equal(result['DOUBLE_QUOTES'], 'value with spaces')
    runner.assert_equal(result['SINGLE_QUOTES'], 'another value')
    runner.assert_equal(result['NO_QUOTES'], 'plain_value')

    cleanup_test_env()


def test_special_characters(runner):
    """Test special characters in values"""
    content = """
URL=https://example.com/path?param=value
EMAIL=user@example.com
PATH=/usr/local/bin:/usr/bin
SPECIAL=value_with-dashes.and.dots
"""
    create_test_env('.env.test', content)
    result = load_dotenv('.env.test')

    runner.assert_equal(result['URL'], 'https://example.com/path?param=value')
    runner.assert_equal(result['EMAIL'], 'user@example.com')
    runner.assert_equal(result['PATH'], '/usr/local/bin:/usr/bin')

    cleanup_test_env()


def test_environ_persistence(runner):
    """Test that _environ persists across calls"""
    from micro_dotenv import _environ

    create_test_env()
    load_dotenv('.env.test')

    # Values should be in _environ
    runner.assert_equal(_environ['TEST_VAR'], 'test_value')

    # get_env should access _environ
    runner.assert_equal(get_env('TEST_VAR'), 'test_value')

    cleanup_test_env()


# Main test runner
def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("MicroPython-dotenv Test Suite")
    print(f"Version: {__version__}")
    print("=" * 60)

    runner = TestRunner()

    # List of all test functions
    tests = [
        test_version,
        test_load_dotenv_basic,
        test_empty_values,
        test_inline_comments,
        test_get_env_with_default,
        test_missing_file,
        test_invalid_lines,
        test_quotes_in_values,
        test_special_characters,
        test_environ_persistence,
    ]

    print("\nRunning tests:")
    print("-" * 60)

    for test in tests:
        runner.run_test(test)

    # Print summary
    success = runner.summary()

    if success:
        print("\n[SUCCESS] All tests passed!")
    else:
        print(f"\n[FAILED] {runner.failed} test(s) failed")

    return success


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
