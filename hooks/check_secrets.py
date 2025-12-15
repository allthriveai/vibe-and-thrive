#!/usr/bin/env python3
"""Pre-commit hook to detect hardcoded secrets and credentials.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

AI agents sometimes hardcode API keys, passwords, and tokens directly in code.
This hook catches common patterns before they're committed.

BLOCKS commits when found (security critical).

Detects:
- API keys (various formats)
- AWS credentials
- Private keys
- Passwords in connection strings
- JWT tokens
- Generic secret patterns
"""

import re
import sys
from pathlib import Path

# Patterns that indicate secrets (compiled pattern, name, severity)
SECRET_PATTERNS = [
    # AWS
    (re.compile(r'AKIA[0-9A-Z]{16}'), 'AWS Access Key ID', 'high'),
    (re.compile(r'aws_secret_access_key\s*=\s*["\'][^"\']+["\']', re.IGNORECASE), 'AWS Secret Key', 'high'),

    # API Keys (generic patterns)
    (re.compile(r'api[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9_\-]{20,}["\']', re.IGNORECASE), 'API Key', 'high'),
    (re.compile(r'apikey\s*[=:]\s*["\'][a-zA-Z0-9_\-]{20,}["\']', re.IGNORECASE), 'API Key', 'high'),

    # Common service keys
    (re.compile(r'sk-[a-zA-Z0-9]{20,}'), 'OpenAI/Stripe Secret Key', 'high'),
    (re.compile(r'pk_live_[a-zA-Z0-9]{20,}'), 'Stripe Publishable Key (Live)', 'medium'),
    (re.compile(r'sk_live_[a-zA-Z0-9]{20,}'), 'Stripe Secret Key (Live)', 'high'),
    (re.compile(r'ghp_[a-zA-Z0-9]{36}'), 'GitHub Personal Access Token', 'high'),
    (re.compile(r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}'), 'GitHub PAT (fine-grained)', 'high'),
    (re.compile(r'xox[baprs]-[a-zA-Z0-9\-]{10,}'), 'Slack Token', 'high'),
    (re.compile(r'hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+'), 'Slack Webhook URL', 'high'),

    # Database connection strings with passwords
    (re.compile(r'postgres://[^:]+:[^@]+@'), 'PostgreSQL connection string with password', 'high'),
    (re.compile(r'mysql://[^:]+:[^@]+@'), 'MySQL connection string with password', 'high'),
    (re.compile(r'mongodb://[^:]+:[^@]+@'), 'MongoDB connection string with password', 'high'),
    (re.compile(r'redis://:[^@]+@'), 'Redis connection string with password', 'high'),

    # Private keys
    (re.compile(r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----'), 'Private Key', 'high'),
    (re.compile(r'-----BEGIN PGP PRIVATE KEY BLOCK-----'), 'PGP Private Key', 'high'),

    # JWT tokens (only if they look real - 3 parts, reasonable length)
    (re.compile(r'eyJ[a-zA-Z0-9_-]{20,}\.eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}'), 'JWT Token', 'medium'),

    # Generic patterns
    (re.compile(r'password\s*[=:]\s*["\'][^"\']{8,}["\']', re.IGNORECASE), 'Hardcoded Password', 'high'),
    (re.compile(r'secret\s*[=:]\s*["\'][a-zA-Z0-9_\-]{16,}["\']', re.IGNORECASE), 'Hardcoded Secret', 'high'),
    (re.compile(r'token\s*[=:]\s*["\'][a-zA-Z0-9_\-]{20,}["\']', re.IGNORECASE), 'Hardcoded Token', 'medium'),
]

# Patterns that indicate false positives (pre-compiled)
FALSE_POSITIVE_PATTERNS = [
    re.compile(r'\.env', re.IGNORECASE),                    # References to .env files
    re.compile(r'process\.env\.', re.IGNORECASE),           # Environment variable access
    re.compile(r'os\.environ', re.IGNORECASE),              # Python env access
    re.compile(r'os\.getenv', re.IGNORECASE),               # Python env access
    re.compile(r'import\.meta\.env', re.IGNORECASE),        # Vite env access
    re.compile(r'example', re.IGNORECASE),                  # Example values
    re.compile(r'placeholder', re.IGNORECASE),              # Placeholder values
    re.compile(r'your[_-]?api[_-]?key', re.IGNORECASE),     # Placeholder patterns
    re.compile(r'xxx+', re.IGNORECASE),                     # Placeholder patterns
    re.compile(r'test[_-]?key', re.IGNORECASE),             # Test values
    re.compile(r'dummy', re.IGNORECASE),                    # Dummy values
    re.compile(r'fake', re.IGNORECASE),                     # Fake values
    re.compile(r'\$\{'),                                    # Template variables
    re.compile(r'<[A-Z_]+>'),                               # Placeholder like <API_KEY>
]

# File patterns to skip (pre-compiled)
SKIP_FILE_PATTERNS = [
    re.compile(r'\.env\.example$'),
    re.compile(r'\.env\.sample$'),
    re.compile(r'\.env\.template$'),
    re.compile(r'package-lock\.json$'),
    re.compile(r'yarn\.lock$'),
    re.compile(r'pnpm-lock\.yaml$'),
    re.compile(r'poetry\.lock$'),
    re.compile(r'Pipfile\.lock$'),
]


def should_skip_file(filepath: Path) -> bool:
    """Check if file should be skipped."""
    filepath_str = str(filepath)
    return any(pattern.search(filepath_str) for pattern in SKIP_FILE_PATTERNS)


def is_false_positive(line: str) -> bool:
    """Check if the line is likely a false positive."""
    return any(pattern.search(line) for pattern in FALSE_POSITIVE_PATTERNS)


def check_file(filepath: Path) -> list[tuple[int, str, str, str]]:
    """Check a file for hardcoded secrets.

    Returns:
        List of (line_number, secret_type, severity, line_preview) tuples
    """
    if should_skip_file(filepath):
        return []

    findings = []

    try:
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # Skip if line looks like a false positive
                if is_false_positive(line):
                    continue

                # Skip comment lines
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('*'):
                    continue

                for pattern, name, severity in SECRET_PATTERNS:
                    match = pattern.search(line)
                    if match:
                        # Redact the actual secret in preview
                        redacted_line = pattern.sub('[REDACTED]', line)
                        preview = redacted_line.strip()[:60]
                        if len(redacted_line.strip()) > 60:
                            preview += '...'
                        findings.append((line_num, name, severity, preview))
                        break

    except Exception as e:
        print(f'Error reading {filepath}: {e}', file=sys.stderr)

    return findings


def main(filenames: list[str]) -> int:
    """Main entry point for pre-commit hook."""
    all_findings: dict[str, list[tuple[int, str, str, str]]] = {}
    has_high_severity = False

    for filename in filenames:
        filepath = Path(filename)
        findings = check_file(filepath)

        if findings:
            all_findings[filename] = findings
            if any(f[2] == 'high' for f in findings):
                has_high_severity = True

    if all_findings:
        total = sum(len(f) for f in all_findings.values())
        file_count = len(all_findings)

        print(f'\n🚨 Potential secrets detected: {total} in {file_count} file(s)\n')

        for filepath, findings in all_findings.items():
            print(f'  {filepath}:')
            for line_num, secret_type, severity, preview in findings:
                icon = '🔴' if severity == 'high' else '🟡'
                print(f'    {icon} Line {line_num}: {secret_type}')
                print(f'       {preview}')

        print('\n⚠️  Never commit secrets to version control!')
        print('   Use environment variables or a secrets manager instead.')
        print('\n   If this is a false positive, you can:')
        print('   - Use a .env.example file with placeholder values')
        print('   - Add the file to .gitignore')

        if has_high_severity:
            print('\n❌ BLOCKING COMMIT due to high-severity findings.\n')
            return 1
        else:
            print('\n⚠️  Warning only (medium severity) - commit will proceed.\n')
            return 0

    return 0


def cli() -> int:
    """CLI entry point."""
    return main(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(cli())
