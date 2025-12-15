# Vibe and Thrive

**Pre-commit hooks and Claude Code tools that help you write better code with AI coding agents.**

When you're vibe coding with Claude, Cursor, Copilot, or other AI assistants, these tools catch common patterns that lead to technical debt—before they hit your codebase.

## What's Included

| Tool | Purpose |
|------|---------|
| **10 Pre-commit Hooks** | Automatically check code at commit time |
| **`/vibe-check` Command** | On-demand code audit in Claude Code |
| **CLAUDE.md Template** | Teach AI agents your standards |

## Quick Start

### Step 1: Install pre-commit

```bash
# macOS
brew install pre-commit

# pip
pip install pre-commit
```

### Step 2: Add hooks to your project

Create `.pre-commit-config.yaml` in your project root:

```yaml
repos:
  - repo: https://github.com/allthriveai/vibe-and-thrive
    rev: v0.1.0
    hooks:
      # Pick the hooks you want:
      - id: check-secrets           # BLOCKS commits with API keys/passwords
      - id: check-hardcoded-urls    # BLOCKS localhost URLs
      - id: check-debug-statements  # Warns about console.log/print
      - id: check-todo-fixme        # Warns about TODO/FIXME comments
      - id: check-empty-catch       # Warns about empty catch blocks
      - id: check-snake-case-ts     # Warns about snake_case in TypeScript
      - id: check-dry-violations-python
      - id: check-dry-violations-js
      - id: check-magic-numbers
      - id: check-docker-platform
```

### Step 3: Install the hooks

```bash
pre-commit install
```

Done! Hooks run automatically on every commit.

### Step 4 (Optional): Add Claude Code integration

```bash
# Clone or download vibe-and-thrive
git clone https://github.com/allthriveai/vibe-and-thrive.git

# Copy the Claude command to your project
cp -r vibe-and-thrive/.claude your-project/

# Copy and customize the CLAUDE.md template
cp vibe-and-thrive/CLAUDE.md.template your-project/CLAUDE.md
```

Now you can run `/vibe-check` in Claude Code anytime.

---

## Updating

### Update hooks to latest version

```bash
cd your-project
pre-commit autoupdate --repo https://github.com/allthriveai/vibe-and-thrive
pre-commit install
```

Or manually update `rev` in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/allthriveai/vibe-and-thrive
    rev: v0.2.0  # Update this to latest
```

### Update Claude commands

Re-copy from the latest vibe-and-thrive:

```bash
git -C vibe-and-thrive pull
cp -r vibe-and-thrive/.claude your-project/
```

---

## Available Hooks

### Hooks That Block Commits

| Hook | What it catches |
|------|-----------------|
| `check-secrets` | API keys, passwords, tokens, private keys |
| `check-hardcoded-urls` | `localhost` and `127.0.0.1` URLs |

### Hooks That Warn Only

| Hook | What it catches |
|------|-----------------|
| `check-debug-statements` | `console.log`, `print()`, `debugger`, `breakpoint()` |
| `check-todo-fixme` | `TODO`, `FIXME`, `XXX`, `HACK`, `BUG` comments |
| `check-empty-catch` | Empty `catch` or `except: pass` blocks |
| `check-snake-case-ts` | `snake_case` properties in TypeScript interfaces |
| `check-dry-violations-python` | Duplicate code blocks, repeated strings, identical functions |
| `check-dry-violations-js` | Same for JS/TS, plus repeated className patterns |
| `check-magic-numbers` | Hardcoded numbers that should be constants |
| `check-docker-platform` | Missing `--platform` in Docker builds (ARM/x86 issues) |

### Suppressing Warnings

Add comments to suppress specific warnings:

```python
print("Starting server...")  # noqa: debug
```

```javascript
console.log('Initializing...'); // noqa: debug
```

---

## Claude Code Integration

### `/vibe-check` Command

Run `/vibe-check` in Claude Code to get a comprehensive report:

```
## Vibe Check Report

### High Priority
- secrets.py:42 - Looks like an API key
- api.ts:15 - localhost URL should use env var

### Medium Priority
- service.py:88 - except: pass (silently swallows errors)
- types.ts:12 - `user_id` should be `userId`

### Low Priority
- utils.py:23 - print() statement
- auth.py:67 - TODO: implement refresh token
```

### CLAUDE.md Template

The template teaches AI agents your coding standards:

- Don't leave debug statements
- Use environment variables for URLs
- Use camelCase in TypeScript
- Handle errors properly
- Complete TODOs before committing
- Never hardcode secrets

Copy and customize for your project's specific patterns.

---

## Configuration

### Excluding Files

Each hook supports standard pre-commit exclude patterns:

```yaml
- id: check-debug-statements
  exclude: |
    (?x)^(
      .*/tests/.*|
      .*\.test\.(ts|js|py)$
    )$
```

### Running Manually

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run check-secrets --all-files

# Run with verbose output
pre-commit run check-dry-violations-python --all-files --verbose
```

---

## Contributing

Found a pattern that AI agents commonly introduce? We'd love to add it!

### Adding a New Hook

1. **Fork the repo**

2. **Create your hook** in `hooks/`:
   ```python
   #!/usr/bin/env python3
   """Pre-commit hook to check for [your pattern]."""

   import sys
   from pathlib import Path

   def check_file(filepath: Path) -> list[tuple[int, str]]:
       # Return list of (line_number, description) tuples
       ...

   def main(filenames: list[str]) -> int:
       # Return 0 for warnings, 1 to block commit
       ...

   if __name__ == '__main__':
       sys.exit(main(sys.argv[1:]))
   ```

3. **Register it** in `.pre-commit-hooks.yaml`:
   ```yaml
   - id: check-your-pattern
     name: Check Your Pattern
     description: What it does
     entry: hooks/check_your_pattern.py
     language: python
     types_or: [python, javascript, ts, tsx]
   ```

4. **Update the README** with documentation

5. **Submit a PR**

### Hook Guidelines

- **Warn by default** - Return `0` to allow commits, `1` only for security issues
- **Be specific** - Catch real problems, not style preferences
- **Allow suppression** - Support `# noqa:` comments
- **Skip tests** - Don't flag test files unless relevant
- **Clear messages** - Tell users what's wrong and how to fix it

### Ideas for New Hooks

- `check-any-types` - TypeScript `any` usage
- `check-function-length` - Functions over 50 lines
- `check-deep-nesting` - 4+ levels of if/for/while
- `check-unused-imports` - Imports that aren't used
- `check-async-await` - Missing `await` on async calls

---

## Philosophy

These hooks are **guardrails, not gatekeepers**. They:

- Warn about most issues (awareness > blocking)
- Block only security-critical problems (secrets, production URLs)
- Support suppression for intentional patterns
- Skip test files where patterns are often acceptable

The goal is to catch AI-generated code issues while staying out of your way.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with love by [AllThrive AI](https://allthrive.ai) for the vibe coding community.
