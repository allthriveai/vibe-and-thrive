# Refactor Code

Guided refactoring with explanations of why each change improves the code.

## Instructions

When asked to refactor code:

### Step 1: Understand Current State

Before changing anything:
1. Read and understand the existing code
2. Identify what it's supposed to do
3. Check for existing tests
4. Note the current patterns in use

### Step 2: Identify Refactoring Opportunities

Look for:

**Structural Issues**
- Functions doing too many things
- Deep nesting
- Long parameter lists
- Feature envy (method uses another class's data more than its own)

**Duplication**
- Copy-pasted code
- Similar functions that could be generalized
- Repeated patterns

**Naming**
- Unclear variable/function names
- Inconsistent naming conventions
- Names that don't match behavior

**Complexity**
- Overly clever code
- Unnecessary abstractions
- Missing abstractions

### Step 3: Plan the Refactoring

Before making changes, explain:
1. What you're going to change
2. Why each change improves the code
3. What risks to watch for

### Step 4: Make Changes Incrementally

For each change:
1. Show the before state
2. Show the after state
3. Explain the improvement
4. Verify behavior is preserved

### Step 5: Verify

After refactoring:
1. Run existing tests (if any)
2. Manually verify the code still works
3. Check that the refactoring achieved its goals

## Output Format

```markdown
## Refactoring: [filename or description]

### Current State
[Brief description of current code and its issues]

### Refactoring Plan
1. [Change 1] - [Why]
2. [Change 2] - [Why]
3. [Change 3] - [Why]

### Change 1: [Description]

**Before:**
```[language]
[original code]
```

**After:**
```[language]
[refactored code]
```

**Why this is better:**
- [Benefit 1]
- [Benefit 2]

### Change 2: [Description]
[... repeat pattern ...]

### Final Result

**Before (complete):**
```[language]
[all original code]
```

**After (complete):**
```[language]
[all refactored code]
```

### Summary of Improvements
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]

### Verification
- [ ] Existing tests pass
- [ ] Behavior unchanged
- [ ] Code is cleaner/simpler
```

## Common Refactorings

### Extract Function
**When:** Code does multiple things or is deeply nested
```python
# Before
def process_order(order):
    # validate
    if not order.items:
        raise Error("No items")
    if not order.customer:
        raise Error("No customer")
    # calculate
    total = sum(item.price for item in order.items)
    # save
    db.save(order)

# After
def process_order(order):
    validate_order(order)
    order.total = calculate_total(order)
    save_order(order)

def validate_order(order):
    if not order.items:
        raise Error("No items")
    if not order.customer:
        raise Error("No customer")
```

### Replace Conditionals with Polymorphism
**When:** Multiple if/else checking type

### Introduce Parameter Object
**When:** Function has many related parameters

### Replace Magic Numbers with Constants
**When:** Hardcoded numbers with unclear meaning

### Simplify Conditionals
**When:** Complex boolean expressions

### Remove Dead Code
**When:** Code that's never executed

## Refactoring Modes

### Safe Refactoring
Only make changes that clearly preserve behavior:
> "Safely refactor this without changing behavior"

### Aggressive Refactoring
Restructure more significantly:
> "Refactor this to follow clean code principles"

### Targeted Refactoring
Fix a specific issue:
> "Refactor to reduce the nesting in this function"

## Important Rules

1. **Never change behavior** while refactoring
2. **Make small changes** - one refactoring at a time
3. **Test after each change** if possible
4. **Explain every change** - this is a teaching tool
5. **Keep it simple** - don't over-engineer
