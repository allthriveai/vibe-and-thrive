"""Pytest configuration for vibe-and-thrive tests."""
import pytest


# Fixtures available to all tests
@pytest.fixture
def sample_python_code():
    """Sample Python code for testing."""
    return '''
def example_function():
    if condition:
        for item in items:
            if another:
                print(item)
'''


@pytest.fixture
def sample_js_code():
    """Sample JavaScript code for testing."""
    return '''
function example() {
    if (condition) {
        for (const item of items) {
            if (another) {
                console.log(item);
            }
        }
    }
}
'''
