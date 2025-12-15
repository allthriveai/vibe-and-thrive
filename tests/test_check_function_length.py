"""Tests for check_function_length.py hook."""
import sys
from pathlib import Path

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'hooks'))

from check_function_length import check_python_file, check_js_file, MAX_FUNCTION_LENGTH


class TestPythonFunctionLength:
    """Tests for Python function length detection."""

    def test_detects_long_function(self, tmp_path):
        """Should detect functions over MAX_FUNCTION_LENGTH lines."""
        test_file = tmp_path / 'long.py'
        # Create a function with 60 lines (over the 50 line limit)
        lines = ['def long_function():']
        for i in range(60):
            lines.append(f'    x = {i}')
        test_file.write_text('\n'.join(lines))

        findings = check_python_file(test_file)

        assert len(findings) == 1
        assert findings[0][1] == 'long_function'
        assert findings[0][2] > MAX_FUNCTION_LENGTH

    def test_allows_short_functions(self, tmp_path):
        """Should not flag functions under the limit."""
        test_file = tmp_path / 'short.py'
        lines = ['def short_function():']
        for i in range(20):
            lines.append(f'    x = {i}')
        test_file.write_text('\n'.join(lines))

        findings = check_python_file(test_file)

        assert len(findings) == 0

    def test_counts_decorators(self, tmp_path):
        """Should include decorators in function length."""
        test_file = tmp_path / 'decorated.py'
        lines = [
            '@decorator1',
            '@decorator2',
            '@decorator3',
            'def decorated_function():'
        ]
        for i in range(50):
            lines.append(f'    x = {i}')
        test_file.write_text('\n'.join(lines))

        findings = check_python_file(test_file)

        # 3 decorators + 1 def + 50 body = 54 lines, over 50
        assert len(findings) == 1


class TestJavaScriptFunctionLength:
    """Tests for JavaScript function length detection."""

    def test_detects_long_function(self, tmp_path):
        """Should detect long functions in JS."""
        test_file = tmp_path / 'long.js'
        lines = ['function longFunction() {']
        for i in range(55):
            lines.append(f'    const x{i} = {i};')
        lines.append('}')
        test_file.write_text('\n'.join(lines))

        findings = check_js_file(test_file)

        assert len(findings) == 1
        assert findings[0][1] == 'longFunction'

    def test_ignores_braces_in_strings(self, tmp_path):
        """Should not miscount braces in string literals."""
        test_file = tmp_path / 'strings.js'
        test_file.write_text('''
function test() {
    const json = '{"key": "value"}';
    const template = `{ braces }`;
    return json;
}
''')

        findings = check_js_file(test_file)

        # Should correctly identify function boundaries
        # This short function should not be flagged
        assert len(findings) == 0

    def test_handles_arrow_functions(self, tmp_path):
        """Should detect long arrow functions."""
        test_file = tmp_path / 'arrow.js'
        lines = ['const longArrow = () => {']
        for i in range(55):
            lines.append(f'    const x{i} = {i};')
        lines.append('};')
        test_file.write_text('\n'.join(lines))

        findings = check_js_file(test_file)

        assert len(findings) == 1

    def test_handles_async_functions(self, tmp_path):
        """Should detect long async functions."""
        test_file = tmp_path / 'async.js'
        lines = ['async function longAsync() {']
        for i in range(55):
            lines.append(f'    const x{i} = {i};')
        lines.append('}')
        test_file.write_text('\n'.join(lines))

        findings = check_js_file(test_file)

        assert len(findings) == 1
        assert findings[0][1] == 'longAsync'
