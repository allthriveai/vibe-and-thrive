"""Tests for check_secrets.py hook."""
import sys
import tempfile
from pathlib import Path

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'hooks'))

from check_secrets import check_file, is_false_positive, should_skip_file


class TestCheckSecrets:
    """Tests for secrets detection."""

    def test_detects_aws_key(self, tmp_path):
        """Should detect AWS access key ID."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('AWS_KEY = "AKIAIOSFODNN7EXAMPLE"')

        findings = check_file(test_file)

        assert len(findings) == 1
        assert findings[0][1] == 'AWS Access Key ID'
        assert findings[0][2] == 'high'

    def test_detects_openai_key(self, tmp_path):
        """Should detect OpenAI API key."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('api_key = "sk-abcdefghijklmnopqrstuvwxyz"')

        findings = check_file(test_file)

        assert len(findings) == 1
        assert 'OpenAI' in findings[0][1] or 'Stripe' in findings[0][1]

    def test_detects_github_token(self, tmp_path):
        """Should detect GitHub personal access token."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('token = "ghp_abcdefghijklmnopqrstuvwxyz0123456789"')

        findings = check_file(test_file)

        assert len(findings) == 1
        assert 'GitHub' in findings[0][1]

    def test_detects_postgres_connection_string(self, tmp_path):
        """Should detect PostgreSQL connection with password."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('DATABASE_URL = "postgres://user:password123@localhost:5432/db"')

        findings = check_file(test_file)

        assert len(findings) >= 1
        assert any('PostgreSQL' in f[1] for f in findings)

    def test_ignores_env_var_reference(self, tmp_path):
        """Should not flag environment variable references."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('api_key = os.getenv("API_KEY")')

        findings = check_file(test_file)

        assert len(findings) == 0

    def test_ignores_process_env(self, tmp_path):
        """Should not flag process.env references."""
        test_file = tmp_path / 'config.js'
        test_file.write_text('const apiKey = process.env.API_KEY;')

        findings = check_file(test_file)

        assert len(findings) == 0

    def test_ignores_example_values(self, tmp_path):
        """Should not flag example/placeholder values."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('api_key = "your-api-key-example"')

        findings = check_file(test_file)

        assert len(findings) == 0

    def test_ignores_comments(self, tmp_path):
        """Should not flag values in comments."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('# API key: sk-abcdefghijklmnopqrstuvwxyz')

        findings = check_file(test_file)

        assert len(findings) == 0

    def test_redacts_secret_in_preview(self, tmp_path):
        """Should redact the actual secret value in the preview."""
        test_file = tmp_path / 'config.py'
        test_file.write_text('AWS_KEY = "AKIAIOSFODNN7EXAMPLE"')

        findings = check_file(test_file)

        assert len(findings) == 1
        # The preview should contain [REDACTED], not the actual key
        preview = findings[0][3]
        assert 'AKIAIOSFODNN7EXAMPLE' not in preview
        assert '[REDACTED]' in preview

    def test_skips_env_example_files(self):
        """Should skip .env.example files."""
        assert should_skip_file(Path('.env.example'))
        assert should_skip_file(Path('config/.env.sample'))
        assert should_skip_file(Path('.env.template'))

    def test_skips_lock_files(self):
        """Should skip lock files."""
        assert should_skip_file(Path('package-lock.json'))
        assert should_skip_file(Path('yarn.lock'))
        assert should_skip_file(Path('poetry.lock'))


class TestFalsePositives:
    """Tests for false positive detection."""

    def test_env_references(self):
        """Should detect .env references as false positives."""
        assert is_false_positive('Load from .env file')
        assert is_false_positive('process.env.API_KEY')
        assert is_false_positive('os.environ["KEY"]')

    def test_placeholder_patterns(self):
        """Should detect placeholder patterns as false positives."""
        assert is_false_positive('your-api-key-here')
        assert is_false_positive('xxx-placeholder-xxx')
        assert is_false_positive('test_key_123')
        assert is_false_positive('dummy_value')
        assert is_false_positive('fake_token')

    def test_template_variables(self):
        """Should detect template variables as false positives."""
        assert is_false_positive('token = "${API_TOKEN}"')
        assert is_false_positive('key = <API_KEY>')
