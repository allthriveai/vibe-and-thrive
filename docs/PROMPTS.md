# Prompt Templates for AI Coding

Copy-paste prompts that get better results from Claude Code, Cursor, Copilot, and other AI coding assistants.

## Quick Reference

| Category | Go-to Prompt |
|----------|--------------|
| [Building UI](#building-ui) | "Use the /styleguide to build..." |
| [Security Review](#security-review) | "Do a security and optimizations review..." |
| [Error Handling](#error-handling) | "How is our error handling..." |
| [Code Review](#code-review) | "Do a code review of that refactor..." |
| [Debugging](#debugging) | "First read the troubleshooting doc, then..." |
| [Testing](#testing) | "Ultrathink through the full user flow..." |
| [DevOps](#devops) | "Make me make commands for..." |

---

## Building UI

### Use Your Styleguide
```
Build the [feature] UI. Use the /styleguide-[name] to make a beautiful,
[adjective] interface.
```

**Example:**
```
Build the frontend battle UI. Use the /styleguide-neon to make a beautiful
react-forward, fun battle interface.
```

### Component with Design System
```
Create a [component] component that follows our design system. Check
/styleguide for colors, spacing, and typography. Make it responsive
and accessible.
```

### Page Layout
```
Build the [page name] page layout. Reference existing pages in /src/pages
for patterns. Include loading states, error states, and empty states.
```

---

## Security Review

### Full Security Audit
```
Do a security and optimizations review. We want:
- User isolation (users can only access their own data)
- No PII leakage
- No silent failures
- Good error logging
- Proper try/catch blocks with meaningful error messages
```

### API Security Check
```
Review this API endpoint for security issues:
- SQL injection
- Authentication/authorization bypass
- Rate limiting
- Input validation
- Sensitive data exposure
```

### Auth Flow Review
```
Review the authentication flow for security issues. Check:
- Token storage and handling
- Session management
- Password handling
- CSRF protection
- OAuth implementation (if applicable)
```

---

## Error Handling

### Error Handling Audit
```
How is our error handling? Check:
- Are we using our logging utility service?
- Are there silent errors (empty catch blocks)?
- Do errors have meaningful messages?
- Are we catching specific exceptions or generic ones?
- Do we have proper error boundaries (React)?
```

### Add Error Handling
```
Add proper error handling to this code:
- Wrap risky operations in try/catch
- Log errors with context (user, action, timestamp)
- Return user-friendly error messages
- Don't expose internal details to users
```

### Fix Silent Failures
```
Find and fix silent failures in [file/directory]. Replace:
- Empty catch blocks with proper error handling
- console.log in catch with proper logging
- Generic "error occurred" with specific messages
```

---

## Code Review

### Post-Refactor Review
```
Do a code review of that refactor. Did we break anything? Check:
- All tests still pass
- No regressions in functionality
- Type safety maintained
- No accidental API changes
- Performance not degraded
```

### PR Review
```
Review this PR for:
- Logic errors
- Edge cases not handled
- Security issues
- Performance concerns
- Code style consistency
- Missing tests
```

### Architecture Review
```
Review this code for architectural issues:
- Separation of concerns
- Single responsibility
- Dependency management
- Testability
- Maintainability
```

---

## Debugging

### Use Documentation First
```
There are [type] issues. First read the [topic] troubleshooting doc in
/docs, then try to solve for:

[paste error message or description]
```

**Example:**
```
There are websocket issues. First read the websocket troubleshooting doc
in /docs, then try to solve for:

WebSocket connection failed: 404
Connection closed unexpectedly after auth
```

### Systematic Debug
```
Debug this issue step by step:
1. What is the expected behavior?
2. What is the actual behavior?
3. What changed recently?
4. Add logging to trace the data flow
5. Identify the root cause
6. Fix and verify
```

### Error Investigation
```
Investigate this error:

[paste error]

1. What does this error mean?
2. What typically causes it?
3. Where in our codebase might this originate?
4. What's the fix?
```

---

## Testing

### User Flow Validation
```
Ultrathink through the full user flow and validate this is working.
Check for edge cases:
- What if the user is not authenticated?
- What if the data is empty?
- What if the request fails?
- What if the user navigates away mid-action?
- What if there's a race condition?
```

### Type Safety Check
```
Check for TypeScript errors and that we are using the global utility
classes. Look for:
- Any `any` types that should be specific
- Missing type definitions
- Inconsistent type usage
- Unused utility functions we should be using
```

### Test Coverage
```
What test coverage do we have for [feature]? What's missing? Write tests for:
- Happy path
- Error cases
- Edge cases
- Integration points
```

---

## DevOps

### Create Make Commands
```
Create make commands for:
- [task 1]
- [task 2]
- [task 3]

Follow the existing Makefile patterns. Include help text.
```

### Pre-commit Check
```
Run the pre-commit hooks as a dry run. Show me what would fail
without actually blocking.
```

### CI/CD Review
```
Review our CI/CD pipeline for:
- Missing checks
- Slow steps that could be parallelized
- Security vulnerabilities
- Caching opportunities
```

---

## Refactoring

### Extract Component
```
This [component/function] is too big. Extract it into smaller,
focused pieces. Each piece should:
- Do one thing well
- Be testable in isolation
- Have clear inputs and outputs
```

### Remove Duplication
```
Find duplicate code in [directory] and consolidate into reusable
utilities. Don't over-abstract - only consolidate if the code is
truly the same, not just similar.
```

### Modernize Code
```
Update this code to use modern patterns:
- Replace callbacks with async/await
- Use destructuring where appropriate
- Replace var with const/let
- Use optional chaining and nullish coalescing
```

---

## Documentation

### Add Code Comments
```
Add comments to this code explaining the "why" not the "what".
Focus on:
- Non-obvious business logic
- Workarounds and their reasons
- Performance considerations
- Security implications
```

### Generate API Docs
```
Generate API documentation for these endpoints. Include:
- Endpoint URL and method
- Request parameters and body
- Response format and status codes
- Example requests and responses
- Error responses
```

---

## Performance

### Performance Audit
```
Review this code for performance issues:
- N+1 queries
- Missing indexes
- Unnecessary re-renders (React)
- Large bundle imports
- Memory leaks
- Blocking operations
```

### Optimize Query
```
This query is slow. Optimize it by:
- Adding appropriate indexes
- Reducing data fetched
- Using pagination
- Caching results where appropriate
```

---

## Pro Tips

### Be Specific
Bad: "Fix the bug"
Good: "Fix the login bug where users get 403 after password reset"

### Provide Context
Bad: "Review this code"
Good: "Review this payment processing code for security issues, especially around handling credit card data"

### Reference Existing Code
Bad: "Create a new component"
Good: "Create a new UserCard component following the pattern in /src/components/ProductCard"

### Ask for Verification
Bad: "Make this change"
Good: "Make this change, then verify it doesn't break the existing tests"

### Chain Your Prompts
```
1. First, read /docs/architecture.md to understand the system
2. Then, review the current implementation in /src/services
3. Finally, propose improvements with specific code changes
```

---

## Template Placeholders

When using these prompts, replace:
- `[feature]` - The feature you're building
- `[component]` - Component name
- `[file/directory]` - Path to code
- `[topic]` - Subject area (websocket, auth, etc.)
- `[type]` - Type of issue (performance, security, etc.)

---

## See Also

- [PROMPTING-GUIDE.md](PROMPTING-GUIDE.md) - How to prompt AI effectively (philosophy)
- [SKILLS.md](SKILLS.md) - Claude Code slash commands (executable prompts)
- [BAD-PATTERNS.md](BAD-PATTERNS.md) - Common AI coding mistakes
- [TDD.md](TDD.md) - Test-driven development workflow
