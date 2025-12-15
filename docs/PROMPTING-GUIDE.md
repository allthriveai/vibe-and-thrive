# Prompting Guide: How to Talk to AI Coding Assistants

The quality of AI-generated code depends heavily on how you ask for it. This guide shows you how to get better results.

---

## The Fundamentals

### 1. Be Specific About Requirements

**Vague prompt:**
> "Build a login form"

**Better prompt:**
> "Build a login form with email and password fields. Include:
> - Client-side validation (email format, password min 8 chars)
> - Error messages shown below each field
> - Loading state on submit button
> - Redirect to /dashboard on success
> - Use our existing Button and Input components from @/components/ui"

### 2. Specify the Tech Stack

AI doesn't always know what libraries you're using.

**Vague:**
> "Add form validation"

**Better:**
> "Add form validation using react-hook-form and zod. Follow the patterns in our existing UserForm component."

### 3. Reference Existing Patterns

**Vague:**
> "Create an API endpoint"

**Better:**
> "Create a POST /api/users endpoint following the same pattern as our existing /api/products endpoint. Use the same error handling and response format."

---

## Power Prompts

### Ask for Tests First (TDD)

> "Before implementing this feature, write the tests first. I want to see the failing tests, then we'll implement the code to make them pass."

This forces AI to think about:
- What the code should do
- Edge cases
- How to verify it works

### Ask "What Could Go Wrong?"

> "What could go wrong with this code? What errors should we handle?"

This prompts AI to consider:
- Network failures
- Invalid input
- Race conditions
- Security issues

### Ask for Explanations

> "Implement this, and explain why you made each decision."

This helps you:
- Learn from the code
- Catch questionable decisions
- Understand trade-offs

### Ask for Alternatives

> "Show me two different ways to implement this, with pros and cons of each."

Useful when:
- You're not sure of the best approach
- Learning new patterns
- Making architectural decisions

---

## Common Scenarios

### When AI Uses `any` Types

**Don't accept this:**
```typescript
function processData(data: any): any {
  return data.items.map((x: any) => x.id);
}
```

**Say:**
> "Don't use `any`. Create proper TypeScript interfaces for this data structure based on the API response."

### When AI Writes Long Functions

**Don't accept 100+ line functions.**

**Say:**
> "This function is doing too many things. Break it into smaller functions, each with a single responsibility."

### When AI Leaves Empty Catch Blocks

**Don't accept:**
```typescript
try { ... } catch (e) {}
```

**Say:**
> "Handle this error properly. Log it, show user feedback, or re-throw. Don't silently swallow errors."

### When AI Hardcodes Values

**Don't accept:**
```typescript
const API_URL = 'http://localhost:3000';
```

**Say:**
> "Use environment variables for configuration. This needs to work in dev, staging, and production."

### When AI Forgets Edge Cases

**Don't accept happy-path-only code.**

**Say:**
> "Add handling for: loading state, error state, empty state, and unauthorized state."

---

## The Review Checklist

Before accepting AI code, ask:

1. **Types**: Are there any `any` types that should be specific?
2. **Length**: Is any function longer than 50 lines?
3. **Errors**: Is every error handled appropriately?
4. **Config**: Are URLs and secrets in environment variables?
5. **Tests**: Is this code tested? Should it be?
6. **Security**: Could this be exploited (XSS, SQL injection, etc.)?
7. **Edge cases**: What happens when things go wrong?

---

## Iteration Patterns

### The Refinement Loop

1. Get initial implementation
2. Ask: "What could be improved?"
3. Apply improvements
4. Repeat until satisfied

### The Challenge Pattern

> "I'm not sure about [specific part]. What are the downsides of this approach? Is there a better way?"

### The Context Addition

When AI misses something:

> "This needs to work with our existing auth system that uses JWT tokens stored in httpOnly cookies. Update the implementation."

### The Constraint Addition

When AI over-engineers:

> "This is simpler than I need. Give me the minimal implementation that just does X."

Or when AI under-engineers:

> "This needs to be production-ready. Add proper error handling, logging, and type safety."

---

## Anti-Patterns to Avoid

### Don't Just Accept First Output

AI's first response is rarely its best. Iterate.

### Don't Skip Understanding

If you don't understand the code, ask AI to explain it. Don't ship code you can't maintain.

### Don't Ignore Warnings

If your linter, type checker, or tests complain, fix the issues. Don't tell AI to "make the errors go away" (it will use hacks like `any` or `// @ts-ignore`).

### Don't Forget Context

AI doesn't remember your whole codebase. Remind it of:
- Existing patterns to follow
- Libraries you're using
- Constraints and requirements

---

## Prompt Templates

### For New Features

```
Implement [feature] that:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Follow the patterns in [existing file]. Use [specific libraries].

Handle these edge cases:
- [Edge case 1]
- [Edge case 2]

Write tests first.
```

### For Bug Fixes

```
There's a bug where [describe the bug].

Expected behavior: [what should happen]
Actual behavior: [what happens instead]

Here's the relevant code: [paste code]

Find the root cause and fix it. Explain why this bug occurred.
```

### For Refactoring

```
Refactor this code to:
- [Goal 1, e.g., "be more testable"]
- [Goal 2, e.g., "follow single responsibility principle"]
- [Goal 3, e.g., "use proper TypeScript types"]

Keep the same functionality. Show me the before/after.
```

### For Code Review

```
Review this code for:
- Security vulnerabilities
- Performance issues
- Error handling gaps
- Code quality issues
- Missing edge cases

Be critical. I want to ship production-quality code.
```

---

## The Meta-Prompt

When you're not sure how to ask for something:

> "I want to [goal]. I'm not sure the best way to approach this. What questions should I answer before we start implementing?"

This gets AI to help you figure out:
- Requirements you haven't considered
- Decisions you need to make
- Constraints that matter
