# Fix Types

Fix TypeScript type errors without using `any`. Create proper interfaces and types.

## Instructions

When asked to fix TypeScript types:

### Step 1: Understand the Error

Read the TypeScript error message carefully:
- What type is expected?
- What type is being provided?
- Where is the mismatch?

### Step 2: Investigate the Data

Before creating types:
1. Check if types already exist elsewhere in the codebase
2. Look at the API response or data source
3. Understand the shape of the data

### Step 3: Create Proper Types

Instead of using `any`, create specific interfaces:

```typescript
// DON'T do this
const data: any = await fetchUser();

// DO this
interface User {
  id: number;
  email: string;
  name: string;
  createdAt: string;
}

const data: User = await fetchUser();
```

### Step 4: Handle Uncertainty

When you don't know the exact type:

**Option 1: Use `unknown` and narrow**
```typescript
function processData(data: unknown) {
  if (isUser(data)) {
    // TypeScript now knows data is User
    console.log(data.email);
  }
}

function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'email' in data &&
    'id' in data
  );
}
```

**Option 2: Use generics**
```typescript
async function fetchData<T>(url: string): Promise<T> {
  const response = await fetch(url);
  return response.json();
}

const user = await fetchData<User>('/api/user');
```

**Option 3: Use partial types for incomplete data**
```typescript
interface UserInput {
  email: string;
  name?: string;  // Optional during creation
}

interface User extends UserInput {
  id: number;
  createdAt: string;
}
```

## Common Type Fixes

### API Response Types
```typescript
// Instead of: const response: any = await api.get('/users')

interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

interface User {
  id: number;
  email: string;
  name: string;
}

const response: ApiResponse<User[]> = await api.get('/users');
```

### Event Handler Types
```typescript
// Instead of: const handleChange = (e: any) => {}

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};
```

### Object with Dynamic Keys
```typescript
// Instead of: const cache: any = {}

const cache: Record<string, User> = {};
// or
const cache: { [key: string]: User } = {};
```

### Union Types for Multiple Possibilities
```typescript
// Instead of: function process(input: any)

type ProcessInput = string | number | Buffer;

function process(input: ProcessInput) {
  if (typeof input === 'string') {
    // TypeScript knows input is string here
  }
}
```

### Third-Party Library Types
```typescript
// If library lacks types, create a declaration file

// types/some-library.d.ts
declare module 'some-library' {
  export function doThing(input: string): Promise<Result>;

  export interface Result {
    success: boolean;
    data: unknown;
  }
}
```

## Output Format

```markdown
## Type Fix: [filename]

### The Error
```
[Original TypeScript error message]
```

### Analysis
[What's causing the error and why]

### Solution

**Step 1: Create interfaces**
```typescript
[New interface definitions]
```

**Step 2: Apply types**

Before:
```typescript
[Original code with any/type errors]
```

After:
```typescript
[Fixed code with proper types]
```

### Why This Is Better
- [Benefit 1: e.g., "IDE autocomplete now works"]
- [Benefit 2: e.g., "Catches typos at compile time"]
- [Benefit 3: e.g., "Documents the data shape"]
```

## Never Use These (Without Good Reason)

| Avoid | Use Instead |
|-------|-------------|
| `any` | Specific type, `unknown`, or generic |
| `@ts-ignore` | Fix the actual type error |
| `as any` | Proper type assertion or type guard |
| `// @ts-nocheck` | Fix file's type errors |

## When `any` Might Be Acceptable

Rare cases where `any` is okay (document why!):

```typescript
// Working with truly dynamic data that can't be typed
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function logAnything(data: any): void {
  console.log(JSON.stringify(data));
}

// Interfacing with untyped third-party library
// TODO: Create proper types when time permits
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const result: any = legacyLibrary.doThing();
```

## Type Inference Tips

Let TypeScript infer when it can:

```typescript
// Unnecessary explicit type
const name: string = 'Alice';  // TypeScript already knows this is string

// Let it infer
const name = 'Alice';

// But DO be explicit for function return types
function getUser(id: number): User | null {
  // ...
}
```
