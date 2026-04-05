# Change Control Gate

## Purpose

Ensure requirement changes are:
- Evaluated for impact
- Approved by appropriate stakeholders
- Tracked for audit
- Communicated to team

---

## Change Types

| Type | Severity | Process |
|------|----------|---------|
| Bug Fix | Low | Quick approval |
| Small Enhancement | Medium | Standard approval |
| Large Feature | High | Extended approval |
| Scope Change | Critical | Requires re-sprint |

---

## Change Request Format

```markdown
# Change Request: {title}

**ID:** CR-{number}
**Date:** {date}
**Requester:** {name}
**Type:** {NEW_REQUIREMENT / BUG_FIX / IMPROVEMENT}
**Status:** {DRAFT / APPROVED / REJECTED / DEFERRED}

## Description
{what is being changed}

## Reason
{why this change is needed}

## Impact Analysis
- **Schedule Impact:** {days/weeks}
- **Cost Impact:** {estimated cost}
- **Technical Impact:** {complexity}

## Affected Items
- PRD: {sections affected}
- Architecture: {components affected}
- Design: {files affected}
- Stories: {related stories}

## Approval
| Role | Name | Decision | Date |
|------|------|----------|------|
| Lead | | | |
| PM | | | |
| Architect | | | |
```

---

## Approval Matrix

| Change Type | Lead | PM | Architect | Customer |
|-------------|------|-----|-----------|----------|
| Bug Fix (P2) | ✓ | | | |
| Bug Fix (P0/P1) | ✓ | ✓ | | |
| Enhancement | ✓ | ✓ | | |
| Scope Change | ✓ | ✓ | ✓ | ✓ |

---

## Decision Options

| Decision | Meaning | Next Action |
|----------|---------|-------------|
| **APPROVED** | Accept change | Implement |
| **REJECTED** | Decline change | Document reason |
| **DEFERRED** | Accept but later | Add to backlog |

---

## Implementation

### After Approval

1. Update PRD
2. Update Architecture
3. Update Design
4. Create/Update Stories
5. Update Sprint plan (if needed)
6. Notify team

### After Rejection

1. Document reason
2. Notify requester
3. No implementation

---

## Tracking

All change requests tracked in `change-log.md`:

```markdown
| ID | Date | Type | Description | Impact | Decision | Sprint |
|----|------|------|-------------|--------|-----------|--------|
| CR-001 | 2026-04-05 | NEW_REQUIREMENT | Add OAuth | Medium | APPROVED | Sprint 02 |
```
