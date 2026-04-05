# Code Review Standards

## Issue Classification

### 🔴 Blocker (Must Fix)

- Security vulnerabilities
- Logic errors
- Critical performance issues
- Breaking changes

### 🟡 Suggestion (Should Fix)

- Readability issues
- Potential optimizations
- Missing comments

### 💭 Nit (Optional)

- Naming inconsistencies
- Formatting issues
- Minor improvements

---

## Review Checklist

| Category | Check |
|----------|-------|
| Correctness | Does code implement requirements? |
| Security | Any vulnerabilities? |
| Performance | Any bottlenecks? |
| Readability | Is code easy to understand? |
| Testing | Sufficient test coverage? |
| Documentation | Are docs updated? |

---

## Feedback Format

```markdown
## Code Review

**Story:** {id}
**Reviewer:** {name}
**Date:** {date}

### 🔴 Blockers

| # | File | Issue | Suggestion |
|---|------|-------|------------|
| 1 | src/api.py | SQL injection risk | Use parameterized queries |

### 🟡 Suggestions

| # | File | Issue | Suggestion |
|---|------|-------|------------|
| 1 | src/utils.js | Missing comments | Add function docs |

### 💭 Nits

- Inconsistent naming
- Formatting issues
```

---

## 3-Strike Rule

**Review failure tracking:**
- Track in `user-stories-tracker.md`
- Each failed review = +1 count

**After 3 failures:**
1. Tech Lead Agent intervenes
2. Analyze root cause
3. Fix directly
4. Continue process

---

## Review Process

```
Submit for review
       ↓
Reviewer checks
       ↓
Blockers found?
    ├── Yes → Record failure count
    │         ↓
    │    Failure count >= 3?
    │    ├── Yes → Human intervention
    │    └── No → Fix → Resubmit
    └── No → Continue
       ↓
   Pass → Merge
```

---

## Security Checks

- SQL injection
- XSS vulnerabilities
- Authentication/Authorization
- Input validation
- Secrets in code
