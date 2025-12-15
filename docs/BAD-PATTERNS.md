# Bad Patterns: A Gallery of AI Coding Mistakes

AI coding assistants are powerful, but they have consistent blind spots. This guide shows you the most common mistakes—and how to fix them.

Each pattern includes:
- What it looks like
- Why it's bad
- How to fix it
- How to prompt AI to do it right

---

## 1. The `any` Escape Hatch

AI loves to use `any` to "fix" TypeScript errors. It's the coding equivalent of putting tape over a check engine light.

### Bad Code
```typescript
// AI's "quick fix" for type errors
function processUser(data: any): any {
  return data.user.profile.name;
}

const result: any = await fetchData();
console.log(result.items.map((x: any) => x.id));
```

### Why It's Bad
- Defeats the entire purpose of TypeScript
- Hides bugs that would be caught at compile time
- Makes refactoring dangerous
- No autocomplete or IDE help

### Good Code
```typescript
interface UserProfile {
  name: string;
  email: string;
}

interface User {
  id: number;
  profile: UserProfile;
}

interface UserResponse {
  user: User;
}

function processUser(data: UserResponse): string {
  return data.user.profile.name;
}
```

### How to Prompt AI
> "Fix this type error without using `any`. Create proper interfaces for the data structure."

> "I'm getting a TypeScript error. Help me create the correct types instead of using `any`."

---

## 2. The Monolithic Function

AI writes functions that do too many things. A single function shouldn't be 200 lines long.

### Bad Code
```python
def process_order(order_data):
    # Validate order (20 lines)
    if not order_data.get('items'):
        raise ValueError("No items")
    if not order_data.get('customer_id'):
        raise ValueError("No customer")
    # ... more validation ...

    # Calculate totals (30 lines)
    subtotal = 0
    for item in order_data['items']:
        price = get_price(item['product_id'])
        quantity = item['quantity']
        subtotal += price * quantity
    # ... tax calculation ...
    # ... discount calculation ...

    # Check inventory (25 lines)
    for item in order_data['items']:
        available = check_inventory(item['product_id'])
        if available < item['quantity']:
            # ... handle backorder ...

    # Process payment (40 lines)
    # ... payment logic ...

    # Send notifications (30 lines)
    # ... email logic ...

    # Update database (25 lines)
    # ... database logic ...

    return result
```

### Why It's Bad
- Hard to test (can't test validation separately from payment)
- Hard to understand (have to read 200 lines to know what it does)
- Hard to reuse (can't reuse just the validation part)
- Hard to debug (which part failed?)

### Good Code
```python
def process_order(order_data: OrderData) -> OrderResult:
    """Process a complete order through validation, payment, and fulfillment."""
    validate_order(order_data)
    totals = calculate_order_totals(order_data)
    check_inventory(order_data.items)
    payment_result = process_payment(order_data.customer_id, totals)
    send_order_confirmation(order_data, payment_result)
    return save_order(order_data, totals, payment_result)

def validate_order(order_data: OrderData) -> None:
    """Validate order has required fields."""
    if not order_data.items:
        raise ValidationError("Order must have at least one item")
    if not order_data.customer_id:
        raise ValidationError("Order must have a customer")

def calculate_order_totals(order_data: OrderData) -> OrderTotals:
    """Calculate subtotal, tax, and final total."""
    subtotal = sum(
        get_price(item.product_id) * item.quantity
        for item in order_data.items
    )
    tax = calculate_tax(subtotal, order_data.shipping_address)
    discount = apply_discounts(subtotal, order_data.promo_code)
    return OrderTotals(subtotal=subtotal, tax=tax, discount=discount)
```

### How to Prompt AI
> "This function is too long. Break it into smaller functions, each doing one thing."

> "Refactor this to follow the single responsibility principle. Each function should be testable in isolation."

---

## 3. The Empty Catch Block

AI often adds try/catch but forgets to actually handle the error.

### Bad Code
```python
try:
    user = get_user(user_id)
    process_user(user)
except Exception:
    pass  # Silently swallow ALL errors
```

```typescript
try {
  await saveData(data);
} catch (e) {
  // AI left this empty
}
```

### Why It's Bad
- Errors happen silently—you'll never know something broke
- Debugging becomes impossible ("it just doesn't work")
- Can leave system in inconsistent state
- Catches errors you didn't expect (like typos in variable names)

### Good Code
```python
try:
    user = get_user(user_id)
    process_user(user)
except UserNotFoundError:
    logger.warning(f"User {user_id} not found, skipping")
    return None
except DatabaseError as e:
    logger.error(f"Database error processing user {user_id}: {e}")
    raise
```

```typescript
try {
  await saveData(data);
} catch (error) {
  if (error instanceof NetworkError) {
    logger.warn('Network error, will retry', { error });
    return retry(saveData, data);
  }
  logger.error('Failed to save data', { error, data });
  throw error;
}
```

### How to Prompt AI
> "Add error handling, but don't use empty catch blocks. Log errors and either recover or re-throw."

> "Handle specific error types differently. Network errors should retry, validation errors should return user feedback."

---

## 4. The Hardcoded URL

AI copies URLs directly into code instead of using configuration.

### Bad Code
```typescript
const API_URL = 'http://localhost:3000/api';

async function fetchUsers() {
  const response = await fetch('http://localhost:3000/api/users');
  return response.json();
}
```

```python
DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"
REDIS_URL = "redis://localhost:6379"
```

### Why It's Bad
- Code won't work in production (different URLs)
- Might accidentally commit production secrets
- Have to change code to deploy to different environments
- Can't run tests against different backends

### Good Code
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

async function fetchUsers() {
  const response = await fetch(`${API_URL}/users`);
  return response.json();
}
```

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/mydb_dev")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
```

### How to Prompt AI
> "Use environment variables for URLs and configuration. Provide sensible defaults for local development."

> "This needs to work in development, staging, and production. Make all URLs configurable."

---

## 5. The Forgotten Console.log

AI leaves debug statements everywhere. Fine for debugging, not for production.

### Bad Code
```typescript
async function processPayment(amount: number) {
  console.log('Processing payment:', amount);

  const result = await paymentGateway.charge(amount);
  console.log('Payment result:', result);
  console.log('DEBUG: got here');

  if (result.success) {
    console.log('Payment successful!');
    return result;
  }

  console.log('Payment failed:', result.error);
  throw new Error(result.error);
}
```

### Why It's Bad
- Clutters production logs with noise
- Can leak sensitive data (imagine logging credit card info)
- Unprofessional in production
- Makes real issues harder to find in logs

### Good Code
```typescript
import { logger } from './logger';

async function processPayment(amount: number) {
  logger.info('Processing payment', { amount });

  const result = await paymentGateway.charge(amount);

  if (result.success) {
    logger.info('Payment successful', { transactionId: result.id });
    return result;
  }

  logger.error('Payment failed', { error: result.error, amount });
  throw new PaymentError(result.error);
}
```

### How to Prompt AI
> "Remove debug console.log statements. Use a proper logger for important events."

> "Add logging, but use appropriate log levels (debug, info, warn, error) and structured data."

---

## 6. The Copy-Paste Duplication

AI repeats the same code instead of extracting it into a function.

### Bad Code
```typescript
// In UserList.tsx
const users = data.filter(item => item.active && item.role === 'user');
const sortedUsers = users.sort((a, b) => a.name.localeCompare(b.name));

// In AdminList.tsx
const admins = data.filter(item => item.active && item.role === 'admin');
const sortedAdmins = admins.sort((a, b) => a.name.localeCompare(b.name));

// In ModeratorList.tsx
const mods = data.filter(item => item.active && item.role === 'moderator');
const sortedMods = mods.sort((a, b) => a.name.localeCompare(b.name));
```

### Why It's Bad
- Bug in one place = bug in all places
- Change in one place = change in all places (if you remember)
- More code to maintain
- Harder to test

### Good Code
```typescript
// In utils/users.ts
function getActiveUsersByRole(users: User[], role: string): User[] {
  return users
    .filter(user => user.active && user.role === role)
    .sort((a, b) => a.name.localeCompare(b.name));
}

// In components
const users = getActiveUsersByRole(data, 'user');
const admins = getActiveUsersByRole(data, 'admin');
const mods = getActiveUsersByRole(data, 'moderator');
```

### How to Prompt AI
> "I see repeated code. Extract the common logic into a reusable function."

> "Apply DRY (Don't Repeat Yourself). What can be extracted and reused?"

---

## 7. The Missing Error Boundary

AI builds happy-path code that crashes when anything goes wrong.

### Bad Code
```typescript
function UserProfile({ userId }: { userId: string }) {
  const { data } = useQuery(['user', userId], fetchUser);

  // What if data is undefined?
  // What if data.profile is null?
  // What if the fetch fails?
  return (
    <div>
      <h1>{data.profile.name}</h1>
      <p>{data.profile.email}</p>
    </div>
  );
}
```

### Why It's Bad
- App crashes on any error
- Users see white screen of death
- No feedback about what went wrong
- Can't recover gracefully

### Good Code
```typescript
function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = useQuery(['user', userId], fetchUser);

  if (isLoading) {
    return <Skeleton />;
  }

  if (error) {
    return <ErrorMessage error={error} retry={() => refetch()} />;
  }

  if (!data?.profile) {
    return <EmptyState message="User not found" />;
  }

  return (
    <div>
      <h1>{data.profile.name}</h1>
      <p>{data.profile.email}</p>
    </div>
  );
}
```

### How to Prompt AI
> "Add loading and error states. Handle the case where data might be missing."

> "What could go wrong here? Add error handling for each failure case."

---

## 8. The Security Vulnerability

AI introduces security holes without realizing it.

### Bad Code
```typescript
// XSS vulnerability
function Comment({ text }: { text: string }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />;
}

// SQL injection
const query = `SELECT * FROM users WHERE name = '${userName}'`;

// Exposing sensitive data
console.log('User data:', { ...user, password: user.password });
```

### Why It's Bad
- XSS lets attackers run JavaScript in your users' browsers
- SQL injection lets attackers access/delete your database
- Logged secrets end up in log aggregators, error trackers, etc.

### Good Code
```typescript
// Safe rendering
function Comment({ text }: { text: string }) {
  return <div>{text}</div>;
}

// Or if you need HTML, sanitize it
import DOMPurify from 'dompurify';
function Comment({ html }: { html: string }) {
  return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(html) }} />;
}

// Parameterized queries
const query = 'SELECT * FROM users WHERE name = $1';
const result = await db.query(query, [userName]);

// Never log sensitive data
const { password, ...safeUser } = user;
logger.info('User data:', safeUser);
```

### How to Prompt AI
> "Review this for security vulnerabilities. Check for XSS, SQL injection, and data exposure."

> "Never use dangerouslySetInnerHTML with user content. Show me a safe alternative."

---

## Quick Reference: Red Flags

When reviewing AI-generated code, watch for:

| Red Flag | What to Do |
|----------|------------|
| `any` type | Ask AI to create proper types |
| Function > 50 lines | Ask AI to break it up |
| `catch (e) {}` | Ask for specific error handling |
| `localhost` URLs | Ask for environment variables |
| `console.log` | Ask for proper logging or removal |
| Repeated code blocks | Ask for extraction into functions |
| No loading/error states | Ask for edge case handling |
| `dangerouslySetInnerHTML` | Ask for safe alternatives |
| String concatenation in queries | Ask for parameterized queries |

---

## The Golden Rule

**Always ask AI: "What could go wrong here?"**

This simple question prompts AI to think about:
- Error cases
- Edge cases
- Security implications
- Performance issues
- Maintainability concerns

The best code handles not just the happy path, but all the ways things can fail.
