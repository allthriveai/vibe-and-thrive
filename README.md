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

| Tool | Purpose |
|------|---------|
| **16 Pre-commit Hooks** | Automatically check code at commit time |
| **9 Claude Code Skills** | `/vibe-check`, `/tdd-feature`, `/review`, etc. |
| **ESLint + Ruff Configs** | Linter configs tuned for AI-generated code |
| **Stack Templates** | CLAUDE.md templates for React, Django, FastAPI, FastMCP, Node |

## Pre-commit Hooks

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/allthriveai/vibe-and-thrive
    rev: v0.2.0
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

## Full Setup

For the complete toolkit (Claude skills, CLAUDE.md template, MCP config):

```bash
git clone https://github.com/allthriveai/vibe-and-thrive.git
./vibe-and-thrive/setup-vibe-and-thrive.sh ~/path/to/your-project
```

## Documentation

| Doc | Description |
|-----|-------------|
| [HOOKS.md](docs/HOOKS.md) | All hooks and configuration options |
| [SKILLS.md](docs/SKILLS.md) | Claude Code skills reference |
| [BAD-PATTERNS.md](docs/BAD-PATTERNS.md) | Common AI mistakes and fixes |
| [PROMPTING-GUIDE.md](docs/PROMPTING-GUIDE.md) | How to prompt AI effectively |
| [WORKFLOW.md](docs/WORKFLOW.md) | TDD workflow for AI coding |
| [CONTRIBUTING.md](docs/CONTRIBUTING.md) | How to add new hooks |

## Philosophy

These are **guardrails, not gatekeepers**:
- Warn about most issues (awareness > blocking)
- Block only security-critical problems
- Support `# noqa:` suppression

## License

MIT - see [LICENSE](LICENSE)

---

Built by [AllThrive AI](https://allthrive.ai) for the vibe coding community.
