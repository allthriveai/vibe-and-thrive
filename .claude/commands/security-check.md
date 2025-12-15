# Security Check

Check code for common security vulnerabilities (OWASP Top 10 and more).

## Instructions

When asked to do a security check:

### Scan for These Vulnerability Categories

#### 1. Injection (Critical)
- **SQL Injection**: String concatenation in queries
- **Command Injection**: User input in shell commands
- **LDAP Injection**: User input in LDAP queries
- **XPath Injection**: User input in XML queries

```python
# VULNERABLE
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# SAFE
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (user_input,))
```

#### 2. Broken Authentication (Critical)
- Hardcoded credentials
- Weak password requirements
- Missing rate limiting on login
- Insecure session management
- Missing MFA for sensitive operations

#### 3. Sensitive Data Exposure (Critical)
- Secrets in code (API keys, passwords)
- Sensitive data in logs
- Unencrypted data transmission
- Sensitive data in URLs
- Missing data encryption at rest

```typescript
// VULNERABLE - logging sensitive data
console.log('User login:', { email, password });

// SAFE
console.log('User login:', { email, password: '[REDACTED]' });
```

#### 4. XML External Entities (XXE) (High)
- XML parsing without disabling external entities
- Accepting XML from untrusted sources

#### 5. Broken Access Control (Critical)
- Missing authorization checks
- IDOR (Insecure Direct Object References)
- Privilege escalation paths
- CORS misconfiguration

```python
# VULNERABLE - no ownership check
def get_document(request, doc_id):
    return Document.objects.get(id=doc_id)

# SAFE
def get_document(request, doc_id):
    return Document.objects.get(id=doc_id, owner=request.user)
```

#### 6. Security Misconfiguration (High)
- Debug mode in production
- Default credentials
- Unnecessary features enabled
- Missing security headers
- Verbose error messages

#### 7. Cross-Site Scripting (XSS) (High)
- Unescaped user content in HTML
- `innerHTML` with user data
- `dangerouslySetInnerHTML` without sanitization
- User data in JavaScript contexts

```typescript
// VULNERABLE
element.innerHTML = userInput;

// SAFE
element.textContent = userInput;
// or with sanitization
element.innerHTML = DOMPurify.sanitize(userInput);
```

#### 8. Insecure Deserialization (High)
- Deserializing untrusted data
- Pickle with untrusted input (Python)
- eval() with user input

```python
# VULNERABLE
data = pickle.loads(user_input)

# SAFE
data = json.loads(user_input)
```

#### 9. Using Components with Known Vulnerabilities (Medium)
- Outdated dependencies
- Unpatched libraries
- Dependencies with known CVEs

#### 10. Insufficient Logging & Monitoring (Medium)
- Missing audit logs for sensitive operations
- No alerting on suspicious activity
- Logs without context for investigation

## Output Format

```markdown
## Security Review: [filename or scope]

### Summary
[Overall security posture: Good/Needs Work/Critical Issues]

### Critical Vulnerabilities
These must be fixed immediately:

#### 1. [Vulnerability Name]
- **Location**: [file:line]
- **Type**: [OWASP category]
- **Risk**: [What an attacker could do]
- **Current Code**:
  ```
  [vulnerable code]
  ```
- **Fix**:
  ```
  [secure code]
  ```

### High-Risk Issues
These should be fixed before production:

#### 1. [Issue Name]
[Same format as above]

### Medium-Risk Issues
Address when possible:

#### 1. [Issue Name]
[Same format as above]

### Recommendations
1. [Security improvement suggestion]
2. [Security improvement suggestion]

### What's Good
[Acknowledge security measures already in place]

### Next Steps
- [ ] [Immediate action item]
- [ ] [Short-term action item]
- [ ] [Long-term action item]
```

## Quick Checks

Run these searches to find common issues:

### Injection
```
- SQL: "SELECT.*FROM.*" + variable
- Command: subprocess, exec, system, shell
- eval(), exec() with variables
```

### XSS
```
- innerHTML =
- dangerouslySetInnerHTML
- document.write
- v-html
```

### Secrets
```
- password =
- api_key =
- secret =
- token =
- AKIA (AWS keys)
- sk- (Stripe/OpenAI keys)
```

### Auth Issues
```
- # TODO: add auth
- # FIXME: check permissions
- @login_required missing
- no authorization check
```

## Security Review Modes

### Quick Scan
Check for obvious critical issues:
> "Quick security scan of the auth module"

### Full Audit
Comprehensive security review:
> "Full security audit of the API endpoints"

### Specific Check
Focus on one vulnerability type:
> "Check for SQL injection vulnerabilities"

### Dependency Audit
Check for vulnerable dependencies:
> "Check our dependencies for known vulnerabilities"

## Important Notes

- **Never commit fixes with example exploits**
- **Don't share specific vulnerability details publicly**
- **Report critical issues to appropriate team members**
- **Security is defense in depth - one fix isn't enough**
