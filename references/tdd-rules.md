# TDD Rules - Test Driven Development

## Core Loop

```
RED → GREEN → REFACTOR

1. RED:     Write a failing test
2. GREEN:   Write minimal code to pass
3. REFACTOR: Improve code structure
```

---

## RED - Write Failing Test

### Rules

- Write test BEFORE writing implementation
- Test describes expected behavior
- Test must fail (because implementation doesn't exist)

### Example

```python
def test_user_can_register():
    user = register_user(email="test@example.com")
    assert user.email == "test@example.com"
```

---

## GREEN - Minimal Implementation

### Rules

- Write MINIMAL code to make test pass
- Don't over-engineer
- Just enough to satisfy the test

### Example

```python
class User:
    def __init__(self, email):
        self.email = email

def register_user(email):
    return User(email=email)
```

---

## REFACTOR - Improve Structure

### Rules

- Improve code without changing behavior
- Keep tests passing
- Remove duplication
- Improve readability

---

## Coverage Requirements

| Type | Minimum |
|------|---------|
| Unit Tests | > 80% |
| Integration Tests | > 60% |
| New Code | 100% |

---

## Test Independence

- Each test can run in any order
- No shared state between tests
- Clean up fixtures after test

---

## Test Naming

```
test_{method}_{scenario}_{expected_result}

Example:
test_user_register_with_valid_email_returns_user
test_user_register_with_duplicate_email_raises_error
```
