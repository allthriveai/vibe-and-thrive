# TDD Feature

Implement a feature using Test-Driven Development: write the failing E2E test first, then build the feature to make it pass.

## Instructions

This skill follows the TDD workflow:
1. **Red**: Write a failing test that defines what success looks like
2. **Green**: Implement the minimum code to make the test pass
3. **Refactor**: Clean up while keeping tests green

### Phase 1: Discovery

Before writing any code, understand the project's testing setup:

**Check for Playwright configuration:**
- Look for `playwright.config.ts` or `playwright.config.js`
- Find the test directory (`e2e/`, `tests/`, etc.)
- Note the base URL configuration

**Check for existing test patterns:**
- Search for `*.spec.ts` or `*.test.ts` files in the test directory
- Look for helper functions and utilities
- Note how auth is handled in existing tests

**Check the tech stack:**
- Frontend framework (React, Vue, etc.)
- API pattern (REST, GraphQL, tRPC)
- Auth mechanism (session/cookie, JWT, OAuth)

### Phase 2: Gather Requirements

Ask the user:
1. **"What feature are you building?"** - Get a clear description
2. **"What should success look like?"** - Define acceptance criteria
3. **"Does this require authentication?"** - Understand auth needs
4. **"What API endpoints will this use?"** - Map the backend requirements

If the user provides a feature description upfront like "Users can reset their password via email", proceed to Phase 3.

### Phase 3: Write the Failing Test (RED)

Create the E2E test file with the SCENARIO/EXPECTED/FAILURE pattern:

```typescript
import { test, expect, Page } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

test.describe('[Feature Name]', () => {

  test('[primary user action]', async ({ page }) => {
    /**
     * SCENARIO: As a [user type], when I [perform action],
     *           I should [see expected outcome]
     * EXPECTED: [Specific, measurable success criteria]
     * FAILURE: [What would indicate the feature is broken]
     */

    // Navigate to the feature
    await page.goto(`${BASE_URL}/feature-path`);

    // Perform user actions
    await page.getByRole('button', { name: /action/i }).click();
    await page.fill('[data-testid="input-field"]', 'test value');
    await page.getByRole('button', { name: /submit/i }).click();

    // Wait for result
    await page.waitForSelector('[data-testid="success-message"]', { timeout: 10000 });

    // Critical assertion with debugging
    const isSuccess = await page.locator('[data-testid="success-message"]').isVisible();
    if (!isSuccess) {
      console.error('FAIL: Success message not visible after form submission');
      await page.screenshot({ path: 'e2e-feature-name-debug.png' });
    }
    expect(isSuccess).toBeTruthy();
  });

});
```

**Key testing patterns:**

1. **Flexible locators** - Handle UI variations:
```typescript
const submitButton = page.getByRole('button', { name: /submit|save|confirm/i })
  .or(page.locator('[data-testid="submit-btn"]'))
  .or(page.locator('button[type="submit"]'));
```

2. **Wait for network** - Don't race with API calls:
```typescript
await Promise.all([
  page.waitForResponse(resp => resp.url().includes('/api/') && resp.status() === 200),
  submitButton.click()
]);
```

3. **Screenshot on failure** - Always capture debug info:
```typescript
if (!condition) {
  console.error('FAIL: Description of what went wrong');
  await page.screenshot({ path: 'e2e-descriptive-name.png' });
}
expect(condition).toBeTruthy();
```

### Phase 4: Run the Test (Confirm RED)

Tell the user to run:
```bash
npx playwright test [test-file] --headed
```

The test should fail because the feature doesn't exist yet. Verify:
- The test fails for the **right reason** (missing UI, 404 endpoint, etc.)
- Not because of test setup issues

If it fails for wrong reasons, fix the test first.

### Phase 5: Implement the Feature (GREEN)

Now implement the minimum code to make the test pass:

1. **Create the UI components** - Only what the test checks for
2. **Create the API endpoints** - Only what the test calls
3. **Wire them together** - Focus on the happy path first

Keep implementation minimal. Don't add:
- Features not covered by the test
- Error handling beyond what's tested
- Optimization or polish

### Phase 6: Run the Test (Confirm GREEN)

```bash
npx playwright test [test-file] --headed
```

The test should now pass. If it doesn't:
- Check the console for errors
- Look at the failure screenshot
- Adjust implementation, not the test (unless test was wrong)

### Phase 7: Refactor (Keep GREEN)

With a passing test as your safety net, now you can:
- Extract reusable components
- Add proper error handling
- Improve code organization
- Add TypeScript types

Run the test after each change to ensure nothing breaks.

### Phase 8: Expand Test Coverage

Add tests for:
- Edge cases (empty inputs, long strings, special characters)
- Error scenarios (network failure, invalid data)
- Auth variations (logged out, different roles)

Each new test follows the same cycle: write failing test → implement → verify.

## Example: Password Reset Feature

**User says:** "Users can reset their password via email"

**Phase 3 - Write failing test:**
```typescript
test.describe('Password Reset', () => {

  test('user can request password reset email', async ({ page }) => {
    /**
     * SCENARIO: As a user who forgot my password, when I enter my email
     *           and click "Reset Password", I should see confirmation
     * EXPECTED: Success message appears, email is sent (mock)
     * FAILURE: Error shown, no confirmation, or page crashes
     */

    await page.goto(`${BASE_URL}/forgot-password`);

    // Enter email
    await page.fill('input[type="email"]', 'test@example.com');

    // Submit request
    await page.getByRole('button', { name: /reset|send/i }).click();

    // Verify success
    const successMessage = page.getByText(/check your email|reset link sent/i);
    await expect(successMessage).toBeVisible({ timeout: 10000 });
  });

  test('shows error for unregistered email', async ({ page }) => {
    /**
     * SCENARIO: As a visitor with an unregistered email, when I request
     *           a password reset, I should see an appropriate message
     * EXPECTED: Message indicating email not found or generic success (for security)
     * FAILURE: Crash, no feedback, or reveals registration status
     */

    await page.goto(`${BASE_URL}/forgot-password`);
    await page.fill('input[type="email"]', 'notregistered@example.com');
    await page.getByRole('button', { name: /reset|send/i }).click();

    // Either error message OR same success message (for security)
    const response = page.getByText(/check your email|not found|no account/i);
    await expect(response).toBeVisible({ timeout: 10000 });
  });

});
```

**Phase 5 - Implement:**
1. Create `/forgot-password` route
2. Create ForgotPasswordForm component
3. Create `POST /api/auth/reset-password` endpoint
4. Wire up form to API

## Notes

- **Test behavior, not implementation** - Tests should pass regardless of how feature is built
- **One feature per test file** - Keep tests focused and fast
- **Independent tests** - Each test sets up its own data, doesn't depend on others
- **Descriptive failures** - Make it easy to debug when tests fail
- **Run tests frequently** - Catch regressions immediately
