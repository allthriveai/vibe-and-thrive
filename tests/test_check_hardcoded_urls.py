"""Tests for check_hardcoded_urls.py hook."""
import sys
from pathlib import Path

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'hooks'))

from check_hardcoded_urls import check_file


class TestHardcodedUrls:
    """Tests for hardcoded URL detection."""

    def test_detects_localhost_url(self, tmp_path):
        """Should detect localhost URLs."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('API_URL = "http://localhost:8000/api"')

        violations = check_file(test_file)

        assert len(violations) == 1
        assert violations[0][0] == 1  # Line 1

    def test_detects_127001_url(self, tmp_path):
        """Should detect 127.0.0.1 URLs."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('API_URL = "http://127.0.0.1:3000/api"')

        violations = check_file(test_file)

        assert len(violations) == 1

    def test_detects_https_localhost(self, tmp_path):
        """Should detect https localhost URLs."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('API_URL = "https://localhost:443/api"')

        violations = check_file(test_file)

        assert len(violations) == 1

    def test_ignores_comments(self, tmp_path):
        """Should not flag URLs in comments."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('# API_URL = "http://localhost:8000/api"')

        violations = check_file(test_file)

        assert len(violations) == 0

    def test_ignores_env_var_fallback(self, tmp_path):
        """Should not flag env var fallback patterns."""
        test_file = tmp_path / 'config.js'
        test_file.write_text('const url = process.env.API_URL || "http://localhost:8000"')

        violations = check_file(test_file)

        assert len(violations) == 0

    def test_ignores_vite_env(self, tmp_path):
        """Should not flag Vite env patterns."""
        test_file = tmp_path / 'config.js'
        test_file.write_text('const url = import.meta.env.VITE_API_URL || "http://localhost:8000"')

        violations = check_file(test_file)

        assert len(violations) == 0

    def test_ignores_os_getenv(self, tmp_path):
        """Should not flag os.getenv patterns."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('API_URL = os.getenv("API_URL", "http://localhost:8000")')

        violations = check_file(test_file)

        assert len(violations) == 0

    def test_ignores_getattr_settings(self, tmp_path):
        """Should not flag Django getattr(settings, ...) patterns."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('API_URL = getattr(settings, "API_URL", "http://localhost:8000")')

        violations = check_file(test_file)

        assert len(violations) == 0
