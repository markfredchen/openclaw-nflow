# E2E Testing Standards

## Screenshot Naming

```
us{story-id}-case{case-id}-step{step}.png

Example:
us001-case001-step1.png   # Story 1, Case 1, Step 1
us001-case001-step2.png   # Story 1, Case 1, Step 2
```

---

## Test Case Format

```markdown
### Test Case: TC-{id}

**Story:** {story_id}
**Description:** {what this tests}

**Preconditions:**
- {condition 1}
- {condition 2}

**Steps:**
1. {action}
2. {action}
3. {action}

**Expected Result:**
- {result 1}
- {result 2}
```

---

## Screenshots

| When | What |
|------|------|
| Before each step | Capture initial state |
| After each step | Capture result |
| On failure | Capture error state |

---

## Test Report

```markdown
# E2E Test Report

**Story:** {id}
**Date:** {date}
**Tester:** {name}

## Results

| TC-ID | Description | Status | Notes |
|-------|-------------|--------|-------|
| TC-001 | Login flow | ✅ PASS | |
| TC-002 | Register | ❌ FAIL | Timeout on step 3 |

## Failed Cases

### TC-002: Register

**Error:** Timeout on step 3
**Screenshot:** us001-case002-step3.png
**Steps to reproduce:**
1. Open registration page
2. Fill form
3. Submit (timeout)
```

---

## Acceptance Report HTML

**Template:** `templates/acceptance-report-template.html`

**Output:** `sprints/sprint-XX/acceptance-report-{id}.html`

**Content:**
- Test summary
- Each test case
- Screenshots for each step
- Pass/fail status

---

## Coverage Requirements

| Type | Minimum |
|------|---------|
| Core user flows | 100% |
| Happy path | 100% |
| Error paths | > 50% |

---

## Best Practices

- Test independence (no shared state)
- Clean environment before test
- Clear pass/fail criteria
- Meaningful test names
- One assertion per test (when possible)
