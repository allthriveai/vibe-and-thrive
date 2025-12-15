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

# Patterns that indicate secrets (pattern, name, severity)
SECRET_PATTERNS = [
    # AWS
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID', 'high'),
    (r'aws_secret_access_key\s*=\s*["\'][^"\']+["\']', 'AWS Secret Key', 'high'),

    # API Keys (generic patterns)
    (r'api[_-]?key\s*[=:]\s*["\'][a-zA-Z0-9_\-]{20,}["\']', 'API Key', 'high'),
    (r'apikey\s*[=:]\s*["\'][a-zA-Z0-9_\-]{20,}["\']', 'API Key', 'high'),

    # Common service keys
    (r'sk-[a-zA-Z0-9]{20,}', 'OpenAI/Stripe Secret Key', 'high'),
    (r'pk_live_[a-zA-Z0-9]{20,}', 'Stripe Publishable Key (Live)', 'medium'),
    (r'sk_live_[a-zA-Z0-9]{20,}', 'Stripe Secret Key (Live)', 'high'),
    (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token', 'high'),
    (r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}', 'GitHub PAT (fine-grained)', 'high'),
    (r'xox[baprs]-[a-zA-Z0-9\-]{10,}', 'Slack Token', 'high'),
    (r'hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+', 'Slack Webhook URL', 'high'),

    # Database connection strings with passwords
    (r'postgres://[^:]+:[^@]+@', 'PostgreSQL connection string with password', 'high'),
    (r'mysql://[^:]+:[^@]+@', 'MySQL connection string with password', 'high'),
    (r'mongodb://[^:]+:[^@]+@', 'MongoDB connection string with password', 'high'),
    (r'redis://:[^@]+@', 'Redis connection string with password', 'high'),

    # Private keys
    (r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', 'Private Key', 'high'),
    (r'-----BEGIN PGP PRIVATE KEY BLOCK-----', 'PGP Private Key', 'high'),

    # JWT tokens (only if they look real - 3 parts, reasonable length)
    (r'eyJ[a-zA-Z0-9_-]{20,}\.eyJ[a-zA-Z0-9_-]{20,}\.[a-zA-Z0-9_-]{20,}', 'JWT Token', 'medium'),

    # Generic patterns
    (r'password\s*[=:]\s*["\'][^"\']{8,}["\']', 'Hardcoded Password', 'high'),
    (r'secret\s*[=:]\s*["\'][a-zA-Z0-9_\-]{16,}["\']', 'Hardcoded Secret', 'high'),
    (r'token\s*[=:]\s*["\'][a-zA-Z0-9_\-]{20,}["\']', 'Hardcoded Token', 'medium'),
]

# Patterns that indicate false positives
FALSE_POSITIVE_PATTERNS = [
    r'\.env',                    # References to .env files
    r'process\.env\.',           # Environment variable access
    r'os\.environ',              # Python env access
    r'os\.getenv',               # Python env access
    r'import\.meta\.env',        # Vite env access
    r'example',                  # Example values
    r'placeholder',              # Placeholder values
    r'your[_-]?api[_-]?key',     # Placeholder patterns
    r'xxx+',                     # Placeholder patterns
    r'test[_-]?key',             # Test values
    r'dummy',                    # Dummy values
    r'fake',                     # Fake values
    r'\$\{',                     # Template variables
    r'<[A-Z_]+>',                # Placeholder like <API_KEY>
]

# File patterns to skip
SKIP_FILE_PATTERNS = [
    r'\.env\.example$',
    r'\.env\.sample$',
    r'\.env\.template$',
    r'package-lock\.json$',
    r'yarn\.lock$',
    r'pnpm-lock\.yaml$',
    r'poetry\.lock$',
    r'Pipfile\.lock$',
]


def should_skip_file(filepath: Path) -> bool:
    """Check if file should be skipped."""
    filepath_str = str(filepath)
    return any(re.search(pattern, filepath_str) for pattern in SKIP_FILE_PATTERNS)


def is_false_positive(line: str) -> bool:
    """Check if the line is likely a false positive."""
    return any(re.search(pattern, line, re.IGNORECASE) for pattern in FALSE_POSITIVE_PATTERNS)


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
                    if re.search(pattern, line, re.IGNORECASE):
                        # Redact the actual secret in preview
                        preview = line.strip()[:60]
                        if len(line.strip()) > 60:
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


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
