# Claude Code Skills Reference

9 slash commands for Claude Code that help with code quality.

## Installation

Copy the skills to your project:

```bash
cp -r vibe-and-thrive/.claude your-project/
```

Or use the setup script:

```bash
./vibe-and-thrive/setup-vibe-and-thrive.sh ~/path/to/your-project
```

## Available Skills

### `/vibe-check`

Full code quality audit. Scans your codebase for common AI-generated issues.

**Output:**
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

### `/tdd-feature`

Implement features using Test-Driven Development:

1. Describe your feature: "Users can reset their password via email"
2. Claude generates a failing Playwright test
3. You run the test, confirm it fails for the right reason
4. Claude implements the feature
5. You run the test again, it passes

The skill adapts to your project's auth patterns, API setup, and existing test helpers.

### `/e2e-scaffold`

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

### `/explain`

Explain code line by line. Great for understanding complex or unfamiliar code.

### `/review`

Review code for issues. Checks for:
- Security vulnerabilities
- Performance problems
- Code smells
- Best practice violations

### `/refactor`

Guided refactoring with explanations. Helps you:
- Extract functions
- Reduce complexity
- Improve naming
- Apply design patterns

### `/add-tests`

Add tests to existing code. Generates:
- Unit tests for functions
- Integration tests for APIs
- Edge case coverage

### `/fix-types`

Fix TypeScript without using `any`. Helps create proper interfaces and types instead of reaching for `any` as a quick fix.

### `/security-check`

Check for OWASP vulnerabilities:
- SQL injection
- XSS
- CSRF
- Insecure dependencies
- Hardcoded secrets

## CLAUDE.md Template

The repo includes a `CLAUDE.md.template` that teaches AI agents your coding standards:

- Don't leave debug statements
- Use environment variables for URLs
- Use camelCase in TypeScript
- Handle errors properly
- Complete TODOs before committing
- Never hardcode secrets

Copy and customize for your project:

```bash
cp vibe-and-thrive/CLAUDE.md.template your-project/CLAUDE.md
```
