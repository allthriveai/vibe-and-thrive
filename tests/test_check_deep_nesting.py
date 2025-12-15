"""Tests for check_deep_nesting.py hook."""
import sys
from pathlib import Path

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'hooks'))

from check_deep_nesting import check_python_file, check_js_file, MAX_NESTING_DEPTH


class TestPythonNesting:
    """Tests for Python deep nesting detection."""

    def test_detects_deep_nesting(self, tmp_path):
        """Should detect nesting deeper than MAX_NESTING_DEPTH."""
        test_file = tmp_path / 'deep.py'
        test_file.write_text('''
def process():
    if condition1:
        if condition2:
            if condition3:
                if condition4:
                    if condition5:
                        print("too deep")
''')

        findings = check_python_file(test_file)

        assert len(findings) > 0
        # Should find nesting deeper than 4 levels
        assert any(depth > MAX_NESTING_DEPTH for _, depth in findings)

    def test_allows_acceptable_nesting(self, tmp_path):
        """Should not flag acceptable nesting levels."""
        test_file = tmp_path / 'ok.py'
        test_file.write_text('''
def process():
    if condition1:
        if condition2:
            if condition3:
                print("this is ok")
''')

        findings = check_python_file(test_file)

        # 3 levels should be fine
        assert len(findings) == 0

    def test_resets_depth_per_function(self, tmp_path):
        """Should reset nesting depth for each function."""
        test_file = tmp_path / 'funcs.py'
        test_file.write_text('''
def func1():
    if a:
        if b:
            pass

def func2():
    if c:
        if d:
            pass
''')

        findings = check_python_file(test_file)

        # Neither function should be flagged (only 2 levels each)
        assert len(findings) == 0


class TestJavaScriptNesting:
    """Tests for JavaScript deep nesting detection."""

    def test_detects_deep_nesting(self, tmp_path):
        """Should detect deep nesting in JS."""
        test_file = tmp_path / 'deep.js'
        test_file.write_text('''
function process() {
    if (condition1) {
        if (condition2) {
            if (condition3) {
                if (condition4) {
                    if (condition5) {
                        console.log("too deep");
                    }
                }
            }
        }
    }
}
''')

        findings = check_js_file(test_file)

        assert len(findings) > 0

    def test_ignores_braces_in_strings(self, tmp_path):
        """Should not count braces inside string literals."""
        test_file = tmp_path / 'strings.js'
        test_file.write_text('''
function test() {
    const str = "{ this { has } braces }";
    if (condition) {
        console.log(str);
    }
}
''')

        findings = check_js_file(test_file)

        # Should not be flagged - only 1 real level
        assert len(findings) == 0

    def test_ignores_braces_in_comments(self, tmp_path):
        """Should not count braces in comments."""
        test_file = tmp_path / 'comments.js'
        test_file.write_text('''
function test() {
    // if (x) { if (y) { if (z) { } } }
    if (condition) {
        console.log("ok");
    }
}
''')

        findings = check_js_file(test_file)

        # Should not be flagged
        assert len(findings) == 0

    def test_handles_template_literals(self, tmp_path):
        """Should handle template literals with braces."""
        test_file = tmp_path / 'template.js'
        test_file.write_text('''
function test() {
    const str = `{ ${value} }`;
    if (condition) {
        console.log(str);
    }
}
''')

        findings = check_js_file(test_file)

        # Should not be flagged
        assert len(findings) == 0
