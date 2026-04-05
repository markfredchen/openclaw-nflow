# Memory Management

## Project Memory Files

### 1. project-memory.md

**Location:** `docs/project-memory.md`

**Purpose:** Global project context

**Content:**
- Project overview
- Sprint progress
- Key decisions
- Known issues
- Technical stack

### 2. decision-log.md

**Location:** `sprints/decision-log.md`

**Purpose:** Audit trail of decisions

**Content:**
- Architecture decisions
- Technology choices
- Design decisions

### 3. Sprint Review

**Location:** `sprints/sprint-XX/review.md`

**Purpose:** Sprint retrospective

**Content:**
- What went well
- Areas for improvement
- Action items

---

## Memory Update Triggers

| Event | Update |
|-------|--------|
| Phase 0 complete | `project-memory.md` |
| Architecture decision | `decision-log.md` |
| New requirement | `change-log.md` |
| Sprint complete | `review.md` + `project-memory.md` |
| Bug discovered | `project-memory.md` (known issues) |

---

## Scripts for Memory

```bash
# Initialize memory
python3 scripts/nflow_tools.py init-memory "Project Name" L2 "OpenClaw"

# Update memory
python3 scripts/nflow_tools.py update-memory sprint_progress=sprint-01

# Log decision
python3 scripts/nflow_tools.py log-decision ARCH "Decision" "Reason"

# Generate context for external agent
python3 scripts/nflow_tools.py generate-context STORY-001
```

---

## Context Injection

When spawning external agents, generate context:

```markdown
## Project Context

**Project:** {name}
**Phase:** Phase 8 (Development)
**Current Sprint:** Sprint 02

**Key Decisions:**
- ARCH-001: FastAPI + PostgreSQL
- ARCH-002: Redis caching

**Known Issues:**
- API pagination not implemented

**Current Story:**
- STORY-001: User registration
- Status: IN_PROGRESS
```

---

## Memory in Commands

Each command should:
1. Read relevant memory before starting
2. Update memory after completing
3. Log significant decisions

---

## Retention

| File | Retention | Archive |
|------|-----------|---------|
| `project-memory.md` | Project lifetime | Keep |
| `decision-log.md` | Project lifetime | Keep |
| `review.md` | Project lifetime | Keep |
| `change-log.md` | Project lifetime | Keep |
