# Vibe and Thrive

**Tools and guardrails that catch common AI coding mistakes before they hit your codebase.**

Whether you're using AI coding agents or building your own agents, MCPs, or applications—these tools catch patterns that lead to technical debt automatically.

## Install

```bash
# Using uv
uv pip install vibe-and-thrive

# Using pip
pip install vibe-and-thrive
```

Then run the setup script to install Claude Code skills, pre-commit hooks, and templates:

```bash
git clone https://github.com/allthriveai/vibe-and-thrive.git
./vibe-and-thrive/setup-vibe-and-thrive.sh ~/path/to/your-project
```

## Usage

### Claude Code (recommended)

Run `/vibe-check` in Claude Code for a full code quality audit:

```
/vibe-check
```

This scans your codebase for secrets, debug statements, empty catches, deep nesting, long functions, and more.

### CLI

```bash
vibe-check-secrets src/         # Hardcoded secrets
vibe-check-urls src/            # Localhost URLs
vibe-check-nesting src/         # Deep nesting
vibe-check-length src/          # Long functions
```

### Pre-commit (automatic)

Runs automatically on every commit. See [Pre-commit Hooks](#pre-commit-hooks) below.

## What's Included

### Claude Code Skills

| Skill | Purpose |
|-------|---------|
| `/vibe-check` | Full code quality audit |
| `/styleguide` | Generate a styleguide from your design preferences |
| `/tdd-feature` | Build features test-first with AI |
| `/e2e-scaffold` | Generate E2E test structure |
| `/review` | Code review for issues |
| `/explain` | Explain code line by line |
| `/refactor` | Guided refactoring |
| `/add-tests` | Add tests to existing code |
| `/fix-types` | Fix TypeScript without `any` |
| `/security-check` | Check for vulnerabilities |

### Also Included

| Tool | Purpose |
|------|---------|
| **16 Pre-commit Hooks** | Automatically check code at commit time |
| **ESLint + Ruff Configs** | Linter configs tuned for AI-generated code |
| **Stack Templates** | CLAUDE.md templates for React, Django, FastAPI, FastMCP, Node |

## Pre-commit Hooks

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/allthriveai/vibe-and-thrive
    rev: v0.3.0
    hooks:
      - id: check-secrets           # BLOCKS commits
      - id: check-hardcoded-urls    # BLOCKS commits
      - id: check-debug-statements  # Warns
      - id: check-empty-catch       # Warns
      - id: check-any-types         # Warns
      - id: check-deep-nesting      # Warns
      - id: check-function-length   # Warns
```

Then: `pre-commit install`

See [docs/HOOKS.md](docs/HOOKS.md) for all 16 hooks.

## Documentation

| Doc | Description |
|-----|-------------|
| [PROMPTS.md](docs/PROMPTS.md) | Copy-paste prompt templates |
| [PROMPTING-GUIDE.md](docs/PROMPTING-GUIDE.md) | How to prompt AI effectively |
| [STYLEGUIDE.md](docs/STYLEGUIDE.md) | Why you need an HTML styleguide |
| [HOOKS.md](docs/HOOKS.md) | All hooks and configuration options |
| [SKILLS.md](docs/SKILLS.md) | Claude Code skills reference |
| [TDD.md](docs/TDD.md) | Test-driven development with AI |
| [BAD-PATTERNS.md](docs/BAD-PATTERNS.md) | Common AI mistakes and fixes |
| [CHEATSHEET.md](docs/CHEATSHEET.md) | Quick reference |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | How to add new hooks |

## Philosophy

These are **guardrails, not gatekeepers**:
- Warn about most issues (awareness > blocking)
- Block only security-critical problems
- Support `# noqa:` suppression
- Little and often make much
- Sleep, code, test, code, sleep, repeat

## License

MIT - see [LICENSE](LICENSE)

---

Built by [AllThrive AI](https://allthrive.ai) for the vibe coding community.
