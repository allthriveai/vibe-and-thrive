# Vibe and Thrive

**Tools and guardrails that catch common AI coding mistakes before they hit your codebase.**

When you're vibe coding with Claude, Cursor, Copilot, or other AI assistants, these tools catch patterns that lead to technical debt—automatically.

## What's Included

| Tool | Purpose |
|------|---------|
| **16 Pre-commit Hooks** | Automatically check code at commit time |
| **9 Claude Code Skills** | On-demand code quality tools |
| **ESLint + Ruff Configs** | Linter configs tuned for AI-generated code |
| **Educational Docs** | Learn to avoid common AI mistakes |
| **Stack Examples** | CLAUDE.md templates for React, Django, Node |
| **Integrations** | Cursor rules, GitHub Actions, VS Code settings |

### Claude Code Skills

| Command | Purpose |
|---------|---------|
| `/vibe-check` | Full code quality audit |
| `/tdd-feature` | TDD workflow (test first, then implement) |
| `/e2e-scaffold` | Generate Playwright test structure |
| `/explain` | Explain code line by line |
| `/review` | Review code for issues |
| `/refactor` | Guided refactoring with explanations |
| `/add-tests` | Add tests to existing code |
| `/fix-types` | Fix TypeScript without using `any` |
| `/security-check` | Check for OWASP vulnerabilities |

## Quick Start

### Option A: Install as a package (recommended)

```bash
# Using uv (fast)
uv pip install vibe-and-thrive

# Or using pip
pip install vibe-and-thrive
```

This gives you CLI commands to run checks directly:

```bash
vibe-check-secrets src/         # Check for hardcoded secrets
vibe-check-urls src/            # Check for localhost URLs
vibe-check-nesting src/         # Check for deep nesting
vibe-check-length src/          # Check for long functions
```

### Option B: One-command setup (full toolkit)

```bash
# Clone vibe-and-thrive
git clone https://github.com/allthriveai/vibe-and-thrive.git

# Run setup for your project
./vibe-and-thrive/setup-vibe-and-thrive.sh ~/path/to/your-project
```

This will:
- Copy 9 Claude Code skills
- Create `CLAUDE.md` from template
- Create `.pre-commit-config.yaml` with all 16 hooks
- Install pre-commit hooks
- Configure Chrome DevTools MCP server for E2E testing

### Option C: Pre-commit hooks only

#### Step 1: Install pre-commit

```bash
# macOS
brew install pre-commit

# Or with uv/pip
uv pip install pre-commit
```

#### Step 2: Add hooks to your project

Create `.pre-commit-config.yaml` in your project root:

```yaml
repos:
  - repo: https://github.com/allthriveai/vibe-and-thrive
    rev: v0.2.0
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

#### Step 3: Install the hooks

```bash
pre-commit install
```

Done! Hooks run automatically on every commit.

#### Step 4 (Optional): Add Claude Code integration

```bash
# Copy the Claude commands to your project
cp -r vibe-and-thrive/.claude your-project/

# Copy and customize the CLAUDE.md template
cp vibe-and-thrive/CLAUDE.md.template your-project/CLAUDE.md
```

Now you can run these commands in Claude Code:
- `/vibe-check` - Code quality audit
- `/tdd-feature` - Build a feature using TDD (write failing test first)
- `/e2e-scaffold` - Generate Playwright E2E test structure

### Setup Script Options

```bash
# Full setup for a project
./setup-vibe-and-thrive.sh ~/Sites/my-project

# Setup current directory
./setup-vibe-and-thrive.sh .

# Only configure MCP servers (no project changes)
./setup-vibe-and-thrive.sh --mcp-only

# Skip MCP configuration
./setup-vibe-and-thrive.sh --no-mcp ~/Sites/my-project

# Skip pre-commit hooks
./setup-vibe-and-thrive.sh --no-hooks ~/Sites/my-project
```

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
| `check-any-types` | TypeScript `any` type usage |
| `check-function-length` | Functions over 50 lines |
| `check-commented-code` | Large blocks of commented-out code |
| `check-deep-nesting` | 4+ levels of nested if/for/while |
| `check-console-error` | `console.log` used for error handling |
| `check-unsafe-html` | `innerHTML`/`dangerouslySetInnerHTML` without sanitization |

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

### TDD Commands

#### `/tdd-feature`

Implement features using Test-Driven Development:

1. Describe your feature: "Users can reset their password via email"
2. Claude generates a failing Playwright test
3. You run the test, confirm it fails for the right reason
4. Claude implements the feature
5. You run the test again, it passes

The skill adapts to your project's auth patterns, API setup, and existing test helpers.

#### `/e2e-scaffold`

Generate a complete E2E test file structure:

```typescript
test.describe('Feature Name', () => {
  test('user can perform action', async ({ page }) => {
    /**
     * SCENARIO: As a user, when I do X, I should see Y
     * EXPECTED: Success criteria
     * FAILURE: What indicates failure
     */
  });
});
```

Includes:
- SCENARIO/EXPECTED/FAILURE documentation pattern
- Screenshot capture on failure
- API helper functions for test data setup
- Flexible locators with fallbacks

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

Have an idea? We'd love contributions:

- `check-unused-imports` - Imports that aren't used
- `check-async-await` - Missing `await` on async calls
- `check-react-keys` - Missing keys in React lists
- `check-sql-injection` - SQL string concatenation

---

## Documentation

### Educational Guides (in `docs/`)

| Doc | What You'll Learn |
|-----|-------------------|
| [BAD-PATTERNS.md](docs/BAD-PATTERNS.md) | Gallery of common AI coding mistakes with fixes |
| [PROMPTING-GUIDE.md](docs/PROMPTING-GUIDE.md) | How to talk to AI to get better code |
| [WORKFLOW.md](docs/WORKFLOW.md) | Step-by-step TDD workflow for AI coding |

### Quick Reference

See [CHEATSHEET.md](CHEATSHEET.md) for a one-page reference of:
- All hooks and what they catch
- All Claude commands
- Common AI mistakes and fixes
- Good prompting patterns

### Stack-Specific Examples (in `examples/`)

| Template | For Projects Using |
|----------|-------------------|
| [CLAUDE-react.md](examples/CLAUDE-react.md) | React, TypeScript, TailwindCSS |
| [CLAUDE-django.md](examples/CLAUDE-django.md) | Django, DRF, PostgreSQL |
| [CLAUDE-node.md](examples/CLAUDE-node.md) | Node.js, Express/Fastify, Prisma |
| [CLAUDE-fullstack.md](examples/CLAUDE-fullstack.md) | React + Django full-stack |

### Integrations (in `integrations/`)

| File | Purpose |
|------|---------|
| [eslint.config.js](integrations/eslint.config.js) | ESLint config for JS/TS (catches AI mistakes) |
| [ruff.toml](integrations/ruff.toml) | Ruff config for Python (linting + formatting) |
| [cursorrules.template](integrations/cursorrules.template) | Rules for Cursor AI |
| [vibe-check.yml](integrations/vibe-check.yml) | GitHub Action for PRs |
| [vscode-settings.json](integrations/vscode-settings.json) | Recommended VS Code settings |

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
