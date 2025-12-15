# Test-Driven Development with AI

## What is TDD in the AI Era?

Test-Driven Development (TDD) is a practice where you write tests before writing code. The classic cycle is: **Red → Green → Refactor**.

1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass the test
3. **Refactor**: Clean up while keeping tests green

With AI coding agents, TDD becomes even more powerful. Instead of writing both the test and implementation yourself, you:

1. **Describe** what you want in plain English
2. **AI writes** a failing test that captures your intent
3. **You verify** the test fails for the right reason
4. **AI implements** code to make it pass
5. **You verify** it works

This keeps you in control while letting AI do the heavy lifting. The test becomes a **contract**—AI can't just generate code that "looks right" but doesn't work.

## Why TDD Matters More with AI

AI coding agents are great at generating code fast, but they often:

- Write code that "looks right" but has subtle bugs
- Skip edge cases
- Create implementations that are hard to test
- Produce code without verifying it works

TDD flips this: **write the test first, then let AI implement to pass it.**

## The TDD Workflow

```
1. Describe what you want
2. AI writes a failing test
3. You verify the test fails for the right reason
4. AI implements the feature
5. You verify the test passes
6. Refactor if needed
```

This gives you:
- **Confidence** - you know the code works
- **Specification** - the test documents behavior
- **Safety net** - catch regressions immediately

## Vibe and Thrive TDD Tools

### `/tdd-feature`

The main TDD skill. Use it like this:

```
/tdd-feature Users can reset their password via email
```

Claude will:
1. Ask clarifying questions if needed
2. Write a failing Playwright E2E test
3. Wait for you to confirm the test fails
4. Implement the feature
5. Wait for you to confirm the test passes

### `/e2e-scaffold`

Generate test structure for a feature:

```
/e2e-scaffold user authentication flow
```

Creates:
```typescript
test.describe('User Authentication', () => {
  test('user can log in with valid credentials', async ({ page }) => {
    /**
     * SCENARIO: User logs in successfully
     * EXPECTED: Redirected to dashboard
     * FAILURE: Error message or stuck on login
     */
  });

  test('user sees error with invalid password', async ({ page }) => {
    /**
     * SCENARIO: User enters wrong password
     * EXPECTED: Error message displayed
     * FAILURE: Logs in anyway or crashes
     */
  });
});
```

### `/add-tests`

Add tests to existing code:

```
/add-tests src/services/auth.ts
```

Generates unit tests for functions that don't have coverage.

## Example: TDD in Practice

### Step 1: Describe the Feature

You: "I want users to be able to bookmark articles"

### Step 2: AI Writes Failing Test

```typescript
// tests/e2e/bookmarks.spec.ts
test('user can bookmark an article', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Navigate to article
  await page.goto('/articles/1');

  // Bookmark it
  await page.click('[data-testid="bookmark-button"]');

  // Verify bookmark saved
  await expect(page.locator('[data-testid="bookmark-button"]')).toHaveAttribute(
    'data-bookmarked',
    'true'
  );

  // Verify in bookmarks list
  await page.goto('/bookmarks');
  await expect(page.locator('article')).toContainText('Article Title');
});
```

### Step 3: You Run the Test

```bash
npx playwright test bookmarks.spec.ts
```

Test fails: `bookmark-button not found` ✓ (expected)

### Step 4: AI Implements

Claude adds:
- Bookmark button component
- API endpoint `POST /api/bookmarks`
- Database model
- Bookmarks list page

### Step 5: You Run Again

```bash
npx playwright test bookmarks.spec.ts
```

Test passes ✓

### Step 6: Refactor

Now you can safely refactor knowing the test will catch any breakage.

## Best Practices

### Write Tests That Fail for the Right Reason

Bad: Test fails because page doesn't load at all
Good: Test fails because the specific feature doesn't exist yet

### Test Behavior, Not Implementation

```typescript
// Bad - tests implementation details
await expect(page.locator('.bookmark-icon-svg-filled')).toBeVisible();

// Good - tests user-visible behavior
await expect(page.getByRole('button', { name: 'Bookmarked' })).toBeVisible();
```

### One Feature Per Test

```typescript
// Bad - tests too much
test('user flow', async ({ page }) => {
  // login, browse, bookmark, unbookmark, logout...
});

// Good - focused
test('user can bookmark article', async ({ page }) => { ... });
test('user can remove bookmark', async ({ page }) => { ... });
```

### Use Test IDs Sparingly

```typescript
// Prefer accessible selectors
page.getByRole('button', { name: 'Save' })
page.getByLabel('Email')
page.getByText('Welcome back')

// Fall back to test IDs when needed
page.locator('[data-testid="complex-widget"]')
```

## Pre-commit Hooks for TDD

These hooks support the TDD workflow:

| Hook | How It Helps |
|------|--------------|
| `check-empty-catch` | Ensures errors aren't silently swallowed |
| `check-console-error` | Catches `console.log` in catch blocks |
| `check-debug-statements` | Removes debug code before commit |
| `check-todo-fixme` | Reminds you to finish incomplete tests |

## CI Integration

Add the GitHub Action to run checks on PRs:

```yaml
# .github/workflows/vibe-check.yml
name: Vibe Check
on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install pre-commit
      - run: pre-commit run --all-files
```

See `integrations/vibe-check.yml` for the full config.

## Resources

- [Playwright Docs](https://playwright.dev)
- [pytest Docs](https://pytest.org)
- [TDD by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) - Kent Beck
