# Vibe and Thrive Cheatsheet

Quick reference for AI-assisted coding best practices.

---

## Pre-commit Hooks

| Hook | What it catches | Blocks? |
|------|-----------------|---------|
| `check-secrets` | API keys, passwords, tokens | Yes |
| `check-hardcoded-urls` | localhost URLs | Yes |
| `check-debug-statements` | console.log, print() | No |
| `check-todo-fixme` | TODO, FIXME comments | No |
| `check-empty-catch` | Empty catch blocks | No |
| `check-snake-case-ts` | snake_case in TypeScript | No |
| `check-dry-violations-python` | Duplicate code (Python) | No |
| `check-dry-violations-js` | Duplicate code (JS/TS) | No |
| `check-magic-numbers` | Hardcoded numbers | No |
| `check-any-types` | TypeScript `any` usage | No |
| `check-function-length` | Functions > 50 lines | No |
| `check-commented-code` | Large commented blocks | No |

**Commands:**
```bash
pre-commit run --all-files          # Run all hooks
pre-commit run check-secrets        # Run specific hook
```

---

## Claude Code Commands

| Command | Purpose |
|---------|---------|
| `/vibe-check` | Full code quality audit |
| `/tdd-feature` | TDD workflow (test first) |
| `/e2e-scaffold` | Generate E2E test structure |
| `/explain` | Explain code line by line |
| `/review` | Review code for issues |
| `/refactor` | Guided refactoring |
| `/add-tests` | Add tests to existing code |
| `/fix-types` | Fix TypeScript without `any` |
| `/security-check` | Check for vulnerabilities |

---

## Common AI Mistakes

| Mistake | Fix |
|---------|-----|
| Uses `any` type | "Create proper interfaces, don't use any" |
| 100+ line function | "Break this into smaller functions" |
| `catch (e) {}` | "Handle the error, don't swallow it" |
| `localhost` URLs | "Use environment variables" |
| `console.log` | "Use proper logging or remove" |
| Copy-paste code | "Extract into reusable function" |
| No error handling | "Add loading, error, empty states" |
| `dangerouslySetInnerHTML` | "Sanitize HTML or use text content" |

---

## Good Prompts

### Be Specific
```
❌ "Build a form"
✅ "Build a login form with email validation,
    error messages, loading state, using
    react-hook-form and our Button component"
```

### Ask for Tests First
```
"Before implementing, write the failing test.
 I want to see it fail, then we'll implement."
```

### Ask What Could Go Wrong
```
"What could go wrong with this code?
 What errors should we handle?"
```

### Reference Existing Patterns
```
"Follow the same pattern as UserForm.tsx"
```

---

## Code Review Checklist

Before committing AI code:

- [ ] No `any` types (unless justified)
- [ ] Functions under 50 lines
- [ ] Errors are handled (not swallowed)
- [ ] URLs use environment variables
- [ ] No console.log in production code
- [ ] No copy-pasted duplicate code
- [ ] Loading/error states handled
- [ ] No security vulnerabilities
- [ ] Tests written (for non-trivial code)

---

## The TDD Workflow

```
1. DESCRIBE  - Tell AI what you want (be specific)
2. TEST      - Write failing test first
3. FAIL      - Run test, confirm it fails correctly
4. IMPLEMENT - Write code to make test pass
5. PASS      - Run test, confirm it passes
6. REVIEW    - Check for issues (/review)
7. COMMIT    - Hooks catch remaining issues
```

---

## Suppress Warnings

When a warning is intentional:

```python
print("Server starting...")  # noqa: debug
```

```typescript
console.log('Initializing...'); // noqa: debug
```

---

## Quick Setup

```bash
# One command setup
./setup-vibe-and-thrive.sh ~/path/to/your-project

# Manual
cp -r .claude your-project/
cp CLAUDE.md.template your-project/CLAUDE.md
pre-commit install
```

---

## Links

- [Bad Patterns Guide](docs/BAD-PATTERNS.md)
- [Prompting Guide](docs/PROMPTING-GUIDE.md)
- [Workflow Guide](docs/WORKFLOW.md)
- [GitHub Repo](https://github.com/allthriveai/vibe-and-thrive)
