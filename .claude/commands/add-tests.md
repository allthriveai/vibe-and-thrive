# Add Tests

Add tests to existing code to improve coverage and confidence.

## Instructions

When asked to add tests:

### Step 1: Analyze the Code

1. Read the code to understand what it does
2. Identify the public interface (what should be tested)
3. Find edge cases and error conditions
4. Check existing test patterns in the project

### Step 2: Determine Test Type

| Code Type | Test Type | Framework |
|-----------|-----------|-----------|
| Utility functions | Unit tests | Jest, pytest |
| React components | Component tests | React Testing Library |
| API endpoints | Integration tests | supertest, pytest |
| User flows | E2E tests | Playwright, Cypress |
| Hooks | Hook tests | @testing-library/react-hooks |

### Step 3: Identify Test Cases

For each function/component, consider:

**Happy Path**
- Normal inputs produce expected outputs
- Main use case works correctly

**Edge Cases**
- Empty inputs
- Null/undefined values
- Boundary values (0, -1, max)
- Single item vs multiple items

**Error Cases**
- Invalid inputs
- Network failures
- Permission errors
- Timeout scenarios

**State Transitions**
- Before/after state changes
- Loading → success → idle
- Loading → error → retry

### Step 4: Write Tests

Use this structure for each test:

```typescript
test('descriptive name of what is being tested', () => {
  // Arrange: Set up test data and conditions
  const input = createTestInput();

  // Act: Perform the action being tested
  const result = functionUnderTest(input);

  // Assert: Verify the expected outcome
  expect(result).toEqual(expectedOutput);
});
```

### Step 5: Document Test Purpose

Use the SCENARIO/EXPECTED/FAILURE pattern:

```typescript
test('user can submit form with valid data', () => {
  /**
   * SCENARIO: User fills out all required fields correctly
   * EXPECTED: Form submits successfully, success message shown
   * FAILURE: Form doesn't submit, or error message shown
   */
});
```

## Output Format

```markdown
## Tests for: [filename]

### Test File Location
`[path/to/test/file.test.ts]`

### Test Cases

1. **Happy Path**: [description]
2. **Edge Case**: [description]
3. **Error Case**: [description]

### Generated Tests

```typescript
[complete test file]
```

### Coverage Summary
- Functions tested: X/Y
- Edge cases covered: [list]
- Not covered (intentionally): [list with reasons]

### Running the Tests
```bash
[command to run tests]
```
```

## Test Patterns

### Unit Test (Function)
```typescript
describe('calculateTotal', () => {
  it('returns sum of item prices', () => {
    const items = [{ price: 10 }, { price: 20 }];
    expect(calculateTotal(items)).toBe(30);
  });

  it('returns 0 for empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('handles single item', () => {
    expect(calculateTotal([{ price: 15 }])).toBe(15);
  });
});
```

### Component Test (React)
```typescript
describe('LoginForm', () => {
  it('submits with valid credentials', async () => {
    const onSubmit = vi.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'password123');
    await userEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('shows error for invalid email', async () => {
    render(<LoginForm onSubmit={vi.fn()} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'invalid');
    await userEvent.click(screen.getByRole('button', { name: /login/i }));

    expect(screen.getByText(/valid email/i)).toBeInTheDocument();
  });
});
```

### API Test (Integration)
```python
def test_create_user_success(client, db):
    """
    SCENARIO: POST /api/users with valid data
    EXPECTED: 201 Created, user in database
    """
    response = client.post('/api/users', json={
        'email': 'test@example.com',
        'name': 'Test User',
    })

    assert response.status_code == 201
    assert User.objects.filter(email='test@example.com').exists()


def test_create_user_duplicate_email(client, db, existing_user):
    """
    SCENARIO: POST /api/users with existing email
    EXPECTED: 400 Bad Request, error message
    """
    response = client.post('/api/users', json={
        'email': existing_user.email,
        'name': 'Another User',
    })

    assert response.status_code == 400
    assert 'already exists' in response.json()['error']
```

### E2E Test (Playwright)
```typescript
test('user can complete checkout', async ({ page }) => {
  /**
   * SCENARIO: User adds item to cart and completes checkout
   * EXPECTED: Order confirmation page shown
   * FAILURE: Stuck on checkout, error message, or wrong page
   */

  // Add item to cart
  await page.goto('/products/1');
  await page.click('button:has-text("Add to Cart")');

  // Go to checkout
  await page.click('a:has-text("Checkout")');

  // Fill shipping info
  await page.fill('[name="address"]', '123 Main St');
  await page.fill('[name="city"]', 'Anytown');

  // Complete order
  await page.click('button:has-text("Place Order")');

  // Verify success
  await expect(page.getByText('Order Confirmed')).toBeVisible();
});
```

## Test Modes

### Quick Tests
Add basic happy path tests:
> "Add basic tests for this function"

### Comprehensive Tests
Full coverage with edge cases:
> "Add comprehensive tests for UserService"

### Specific Scenario
Test a specific case:
> "Add a test for when the API returns a 404"

## Tips

- **Test behavior, not implementation**
- **One assertion per test** (when possible)
- **Use descriptive test names**
- **Don't test framework code** (React, Django, etc.)
- **Mock external dependencies**
- **Keep tests fast**
