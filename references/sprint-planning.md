# Sprint Planning

## Sprint Structure

```
Sprint
├── Planning
├── Execution
├── Daily Standup
├── Review
└── Retrospective
```

---

## Sprint Planning

### Inputs
- Product Backlog
- Velocity from previous sprints
- Team capacity

### Outputs
- Sprint Backlog
- Sprint Goal
- Sprint Plan

---

## Story Points

### Fibonacci Scale

| Points | Complexity | Time |
|--------|-----------|------|
| 1 | Trivial | ~1 hour |
| 2 | Simple | ~2-4 hours |
| 3 | Medium | ~1 day |
| 5 | Complex | ~2-3 days |
| 8 | Very Complex | ~1 week |
| 13 | Epic | > 1 week |

### Velocity

```
Velocity = Total story points completed per sprint

Example:
Sprint 01: 21 points
Sprint 02: 24 points
Sprint 03: 20 points

Average Velocity = (21 + 24 + 20) / 3 = 21.67
```

---

## Sprint Capacity

### Calculation

```
Available Hours = Team Members × Days × Hours per Day
Available Hours -= Meetings, Reviews, Breaks

Example:
3 developers × 10 days × 6 hours = 180 hours

Story Points = Available Hours / Average hours per point
```

---

## Sprint Selection

### Priority Rules

1. **Dependency** - Stories with dependencies first
2. **Priority** - P0 > P1 > P2 > P3
3. **Capacity** - Don't overcommit

### Anti-patterns

- ❌ Selecting stories without understanding
- ❌ Ignoring dependencies
- ❌ Overcommitting
- ❌ Last minute additions

---

## Definition of Done

| Criteria | Description |
|----------|-------------|
| Code Complete | All code written and reviewed |
| Tests Pass | Unit + Integration + E2E |
| Deployed | Successfully deployed to staging |
| Accepted | PM acceptance sign-off |

---

## Sprint Board

| Column | Meaning |
|--------|---------|
| TODO | Selected for sprint, not started |
| IN PROGRESS | Currently being worked |
| CODE REVIEW | Under review |
| TESTING | Being tested |
| DONE | Completed and accepted |
