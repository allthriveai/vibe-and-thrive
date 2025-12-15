# E2E Test Scaffold

Generate a Playwright E2E test file structure for a new feature.

## Instructions

Before generating the scaffold, **discover the project's testing setup**:

### Step 1: Discovery Phase

Check for existing patterns in this order:

1. **Playwright config**: Look for `playwright.config.ts` or `playwright.config.js`
   - Note the `testDir` setting
   - Check for `baseURL` configuration
   - Look for any custom fixtures or global setup

2. **Test directory structure**: Search for existing E2E tests
   - Common locations: `e2e/`, `tests/`, `tests/e2e/`, `__tests__/e2e/`
   - Note the file naming pattern (`.spec.ts`, `.test.ts`, etc.)

3. **Existing helpers**: Look for helper files
   - `e2e/helpers.ts`, `tests/helpers.ts`, `tests/utils.ts`
   - Note API call patterns, auth setup, common utilities

4. **Auth patterns**: Search for how tests handle authentication
   - Session-based with cookies
   - JWT tokens
   - OAuth flows
   - No auth needed

5. **API patterns**: Check the tech stack
   - REST endpoints
   - GraphQL queries
   - tRPC calls

### Step 2: Ask User

If patterns are unclear, ask:
- "What feature are you building tests for?"
- "Does this feature require authentication?"
- "What API endpoints will the feature use?"

### Step 3: Generate Scaffold

Create a test file with this structure:

```typescript
import { test, expect, Page } from '@playwright/test';

// Configuration - adapt to project's pattern
const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * [Add helper functions for API calls, auth setup, etc.]
 *
 * Example API helper pattern:
 * async function createResourceViaAPI(page: Page): Promise<{ id: number }> {
 *   const result = await page.evaluate(async (apiBase) => {
 *     const response = await fetch(`${apiBase}/api/v1/resources/`, {
 *       method: 'POST',
 *       headers: { 'Content-Type': 'application/json' },
 *       credentials: 'include',
 *     });
 *     return response.json();
 *   }, API_BASE_URL);
 *   return result;
 * }
 */

// ============================================================================
// TEST SUITE: [Feature Name]
// ============================================================================

test.describe('[Feature Name]', () => {

  test.beforeEach(async ({ page }) => {
    // Setup: navigate to the feature, log in if needed
    await page.goto(BASE_URL);
  });

  test.afterEach(async ({ page }, testInfo) => {
    // Capture screenshot on failure for debugging
    if (testInfo.status !== testInfo.expectedStatus) {
      const screenshotPath = `e2e-${testInfo.title.replace(/\s+/g, '-')}-failure.png`;
      await page.screenshot({ path: screenshotPath });
      console.log(`Screenshot saved: ${screenshotPath}`);
    }
  });

  // --------------------------------------------------------------------------
  // Happy Path Tests
  // --------------------------------------------------------------------------

  test('user can [primary action]', async ({ page }) => {
    /**
     * SCENARIO: As a [user type], when I [action],
     *           I should [expected outcome]
     * EXPECTED: [Specific success criteria]
     * FAILURE: [What would indicate failure]
     */

    // Arrange: Set up test data

    // Act: Perform user actions

    // Assert: Verify expected outcome
    // Use the critical assertion pattern:
    // const isSuccess = await page.locator('[data-testid="success"]').isVisible();
    // if (!isSuccess) {
    //   console.error('FAIL: Success indicator not visible');
    //   await page.screenshot({ path: 'e2e-test-name-debug.png' });
    // }
    // expect(isSuccess).toBeTruthy();
  });

  // --------------------------------------------------------------------------
  // Edge Cases
  // --------------------------------------------------------------------------

  test('handles [edge case scenario]', async ({ page }) => {
    /**
     * SCENARIO: As a [user type], when [edge case condition],
     *           I should [expected behavior]
     * EXPECTED: [Specific handling criteria]
     * FAILURE: [What would indicate improper handling]
     */
  });

  // --------------------------------------------------------------------------
  // Error Handling
  // --------------------------------------------------------------------------

  test('shows error when [error condition]', async ({ page }) => {
    /**
     * SCENARIO: As a [user type], when [error condition occurs],
     *           I should see an appropriate error message
     * EXPECTED: Error message displayed, user can recover
     * FAILURE: Silent failure, crash, or unclear error
     */
  });

});
```

### Step 4: Adapt to Project

Based on discovery, customize the scaffold:

**If project uses session auth with CSRF:**
```typescript
async function apiCallWithAuth(page: Page, endpoint: string, method: string, body?: object) {
  return await page.evaluate(async ({ apiBase, endpoint, method, body }) => {
    const csrfToken = document.cookie.split('; ')
      .find(row => row.startsWith('csrftoken='))?.split('=')[1];
    const response = await fetch(`${apiBase}${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken || ''
      },
      credentials: 'include',
      body: body ? JSON.stringify(body) : undefined,
    });
    return response.json();
  }, { apiBase: API_BASE_URL, endpoint, method, body });
}
```

**If project uses JWT:**
```typescript
async function apiCallWithJWT(page: Page, endpoint: string, method: string, body?: object) {
  return await page.evaluate(async ({ apiBase, endpoint, method, body }) => {
    const token = localStorage.getItem('authToken');
    const response = await fetch(`${apiBase}${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    return response.json();
  }, { apiBase: API_BASE_URL, endpoint, method, body });
}
```

**If project has existing helpers, import them:**
```typescript
import { loginAsTestUser, createTestData, cleanupTestData } from './helpers';
```

### Step 5: Output

Provide:
1. The scaffold file at the appropriate location
2. Summary of discovered patterns used
3. List of placeholder TODOs for the user to complete
4. Suggestion to run `npx playwright test --ui` to verify setup

## Notes

- Always use the SCENARIO/EXPECTED/FAILURE documentation pattern
- Include screenshot capture on failure
- Use flexible locators: `page.getByRole()` with `.or()` for fallbacks
- Keep tests independent - each test should set up its own data
- Use `test.describe()` to group related tests
