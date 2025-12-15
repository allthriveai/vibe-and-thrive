# The Vibe Coding Workflow

A step-by-step process for building production-quality code with AI assistants.

---

## The 7-Step Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  1. DESCRIBE  →  2. TEST  →  3. FAIL  →  4. IMPLEMENT  →   │
│                                                             │
│  5. PASS  →  6. REVIEW  →  7. COMMIT                        │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Describe What You Want

Be specific. The more detail you give AI, the better the result.

**Bad:**
> "Add user authentication"

**Good:**
> "Add user authentication with:
> - Email/password login
> - JWT tokens stored in httpOnly cookies
> - Protected routes that redirect to /login
> - Remember me checkbox (extends token to 30 days)
> - Follow our existing API patterns in /api/v1/"

**Tips:**
- List all requirements
- Mention existing patterns to follow
- Specify libraries to use
- Note any constraints

### Step 2: Write the Test First

Ask AI to write a failing test before implementing anything.

> "Before writing the implementation, write the E2E test for this feature. Use Playwright and follow our test patterns."

**Why test first?**
- Forces you to think about what "done" looks like
- Catches misunderstandings before you write code
- Creates documentation of expected behavior
- Makes you consider edge cases

**Example test:**
```typescript
test('user can log in with valid credentials', async ({ page }) => {
  /**
   * SCENARIO: User submits valid email and password
   * EXPECTED: Redirected to dashboard, see welcome message
   * FAILURE: Still on login page, or error message shown
   */

  await page.goto('/login');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'validpassword123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
  await expect(page.getByText('Welcome back')).toBeVisible();
});
```

### Step 3: Run the Test (Confirm Failure)

Run the test to confirm it fails for the right reason.

```bash
npx playwright test auth.spec.ts --headed
```

**Why confirm failure?**
- Ensures the test actually tests something
- Catches tests that accidentally pass
- Verifies test setup is correct

**Right reason to fail:**
- "Element not found" (UI doesn't exist yet)
- "404 Not Found" (API endpoint doesn't exist)

**Wrong reason to fail:**
- Test syntax error
- Wrong selector
- Incorrect test setup

If it fails for the wrong reason, fix the test first.

### Step 4: Implement the Feature

Now ask AI to implement the feature.

> "The test is failing because the login form doesn't exist. Implement the login feature to make this test pass."

**Tips:**
- Keep implementation minimal (just enough to pass the test)
- Don't add extra features not covered by tests
- Follow existing patterns in the codebase

### Step 5: Run the Test (Confirm Pass)

```bash
npx playwright test auth.spec.ts --headed
```

**If it passes:** Move to Step 6.

**If it fails:**
- Check the failure message
- Look at screenshots (if captured)
- Ask AI to debug: "The test is still failing. Here's the error: [error]. What's wrong?"

### Step 6: Review the Code

Before committing, review what AI wrote.

> "Review this implementation for:
> - Security issues
> - Error handling gaps
> - Code quality problems
> - Missing edge cases"

**Or use the `/review` command in Claude Code.**

**Common issues to catch:**
- `any` types in TypeScript
- Empty catch blocks
- Hardcoded URLs
- Missing loading/error states
- Console.log statements

### Step 7: Commit

The pre-commit hooks will catch remaining issues.

```bash
git add .
git commit -m "Add user authentication with email/password"
```

**If hooks fail:**
- Read the error message
- Fix the issue (or ask AI to help)
- Try committing again

**If hooks warn:**
- Decide if the warning is valid
- Fix it or add a suppression comment with explanation

---

## Quick Reference

| Step | Action | Tool |
|------|--------|------|
| 1. Describe | Tell AI what you want | Chat |
| 2. Test | Write failing test | `/tdd-feature` |
| 3. Fail | Confirm test fails correctly | `npx playwright test` |
| 4. Implement | Build the feature | Chat |
| 5. Pass | Confirm test passes | `npx playwright test` |
| 6. Review | Check for issues | `/review` |
| 7. Commit | Save your work | `git commit` |

---

## Workflow Variations

### For Bug Fixes

1. **Reproduce**: Write a test that fails because of the bug
2. **Fix**: Implement the fix
3. **Verify**: Test passes
4. **Prevent**: Test ensures bug won't come back

### For Refactoring

1. **Cover**: Ensure existing tests pass
2. **Refactor**: Make changes
3. **Verify**: Tests still pass
4. **Review**: Check for improvements

### For Quick Changes

Not everything needs full TDD. For trivial changes:

1. Make the change
2. Run `/vibe-check`
3. Commit

Use judgment—but when in doubt, write a test.

---

## Common Pitfalls

### Skipping Tests

"I'll add tests later" = "I'll never add tests"

Tests are easier to write when the requirements are fresh in your mind.

### Testing Implementation, Not Behavior

**Bad test:**
```typescript
test('calls the API', async () => {
  expect(mockApi.calls.length).toBe(1);
});
```

**Good test:**
```typescript
test('shows user name after login', async () => {
  await login(page, 'test@example.com');
  await expect(page.getByText('Welcome, Test User')).toBeVisible();
});
```

Test what the user sees, not how the code works internally.

### Accepting AI's First Response

AI's first attempt is rarely optimal. Iterate:

1. Get initial implementation
2. Ask "What could be improved?"
3. Apply improvements
4. Ask "What edge cases are missing?"
5. Add edge case handling

### Not Reading the Code

If you don't understand it, don't ship it. Ask AI to explain:

> "Explain this code line by line. Why did you make each decision?"

---

## The Goal

After following this workflow, you should have:

- **Working code** that does what you asked
- **Tests** that prove it works
- **Clean code** that's reviewed for issues
- **Version control** with meaningful commits

Ship confidently. The guardrails have your back.
