# Pre-commit Hooks Reference

All 16 hooks available in vibe-and-thrive.

## Hooks That Block Commits

These hooks return exit code 1 to prevent commits with security issues.

| Hook | What it catches |
|------|-----------------|
| `check-secrets` | API keys, passwords, tokens, private keys |
| `check-hardcoded-urls` | `localhost` and `127.0.0.1` URLs |

## Hooks That Warn Only

These hooks warn but allow commits to proceed.

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
| `check-any-types` | TypeScript `any` type usage |
| `check-function-length` | Functions over 50 lines |
| `check-commented-code` | Large blocks of commented-out code |
| `check-deep-nesting` | 4+ levels of nested if/for/while |
| `check-console-error` | `console.log` used for error handling |
| `check-unsafe-html` | `innerHTML`/`dangerouslySetInnerHTML` without sanitization |

## Full Configuration

```yaml
repos:
  - repo: https://github.com/allthriveai/vibe-and-thrive
    rev: v0.2.0
    hooks:
      # Security (blocks commits)
      - id: check-secrets
      - id: check-hardcoded-urls

      # Code quality (warnings)
      - id: check-debug-statements
      - id: check-todo-fixme
      - id: check-empty-catch
      - id: check-snake-case-ts
      - id: check-dry-violations-python
      - id: check-dry-violations-js
      - id: check-magic-numbers
      - id: check-docker-platform

      # AI-specific issues (warnings)
      - id: check-any-types
      - id: check-function-length
      - id: check-commented-code
      - id: check-deep-nesting
      - id: check-console-error
      - id: check-unsafe-html
```

## Excluding Files

Each hook supports standard pre-commit exclude patterns:

```yaml
- id: check-debug-statements
  exclude: |
    (?x)^(
      .*/tests/.*|
      .*\.test\.(ts|js|py)$
    )$
```

## Suppressing Warnings

Add comments to suppress specific warnings:

```python
print("Starting server...")  # noqa: debug
```

```javascript
console.log('Initializing...'); // noqa: debug
```

## Running Manually

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run check-secrets --all-files

# Run with verbose output
pre-commit run check-dry-violations-python --all-files --verbose
```

## CLI Commands

If you install via pip/uv, you get CLI commands:

```bash
vibe-check-secrets src/
vibe-check-urls src/
vibe-check-debug src/
vibe-check-todo src/
vibe-check-catch src/
vibe-check-dry src/
vibe-check-nesting src/
vibe-check-length src/
vibe-check-comments src/
vibe-check-console src/
vibe-check-magic src/
```

## Updating

```bash
pre-commit autoupdate --repo https://github.com/allthriveai/vibe-and-thrive
pre-commit install
```
