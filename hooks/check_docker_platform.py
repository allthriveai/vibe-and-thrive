#!/usr/bin/env python3
"""Pre-commit hook to check Docker configurations for architecture compatibility.

Part of vibe-and-thrive: https://github.com/allthriveai/vibe-and-thrive

This hook ensures:
1. Dockerfile.prod specifies explicit platform for multi-arch builds
2. docker-compose files don't accidentally override production architecture
3. Any docker build commands in scripts specify the correct platform

This is especially important when developing on Apple Silicon (ARM) but
deploying to x86_64 servers (AWS ECS, most cloud providers).
"""

import re
import sys
from pathlib import Path


def check_dockerfile_prod(filepath: Path) -> list[str]:
    """Check Dockerfile.prod for architecture safety."""
    errors = []
    content = filepath.read_text()

    has_platform_spec = '--platform' in content

    if not has_platform_spec:
        if 'platform' not in content.lower():
            errors.append(
                f'{filepath}: Production Dockerfile should specify platform explicitly.\n'
                f"  Add '--platform=linux/amd64' to FROM statements or add a comment\n"
                f'  explaining how architecture is handled (e.g., in CI/CD).'
            )

    return errors


def check_scripts_for_docker_build(filepath: Path) -> list[str]:
    """Check shell scripts for docker build commands without platform."""
    errors = []
    content = filepath.read_text()

    docker_build_pattern = r'docker\s+build[^|&;\n]*'
    builds = re.findall(docker_build_pattern, content, re.IGNORECASE)

    for build_cmd in builds:
        if build_cmd.strip().startswith('#'):
            continue

        if '--platform' not in build_cmd and 'buildx' not in build_cmd:
            if 'prod' in build_cmd.lower() or 'Dockerfile.prod' in build_cmd:
                errors.append(
                    f'{filepath}: Docker build command for production should specify platform.\n'
                    f'  Found: {build_cmd.strip()}\n'
                    f'  Add: --platform=linux/amd64'
                )

    return errors


def check_docker_compose_platform(filepath: Path) -> list[str]:
    """Check docker-compose files for platform specifications."""
    errors = []
    content = filepath.read_text()

    if 'Dockerfile.prod' in content or 'dockerfile: Dockerfile.prod' in content.lower():
        if 'platform:' not in content:
            errors.append(
                f"{filepath}: Uses Dockerfile.prod but doesn't specify platform.\n"
                f"  For production builds, add 'platform: linux/amd64' to the service."
            )

    return errors


def main() -> int:
    """Main entry point."""
    errors = []

    for arg in sys.argv[1:]:
        filepath = Path(arg)

        if not filepath.exists():
            continue

        filename = filepath.name.lower()

        if filename == 'dockerfile.prod':
            errors.extend(check_dockerfile_prod(filepath))
        elif filename.endswith('.sh'):
            errors.extend(check_scripts_for_docker_build(filepath))
        elif 'docker-compose' in filename and filename.endswith(('.yml', '.yaml')):
            errors.extend(check_docker_compose_platform(filepath))

    if errors:
        print('Docker Architecture Check Failed!')
        print('=' * 50)
        print()
        print('AWS ECS and most cloud providers run on linux/amd64 (x86_64).')
        print('Building on Apple Silicon (ARM) without specifying platform')
        print("will cause 'exec format error' in production.")
        print()
        for error in errors:
            print(f'ERROR: {error}')
            print()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
