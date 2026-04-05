# NFlow - Custom Development Workflow 🏗️

**Version:** 1.0.0  
**Fusion:** BMad Method + Superpowers  
**Platforms:** OpenClaw / Claude Code / Codex / Gemini

---

## Why NFlow

- **Structured Development** — 10 commands covering the full lifecycle from requirements to deployment
- **TDD Development** — RED → GREEN → REFACTOR enforced loop
- **Multi-Agent Collaboration** — 16 specialized agents with clear responsibilities
- **Change Control** — Change Control Gate ensures requirement stability
- **Memory Management** — Project memory persists across sessions
- **Lazy-Loading** — Load knowledge only when needed

---

## Best For

- Building complex projects from scratch
- Medium-to-large projects requiring multi-agent collaboration
- Teams追求 TDD and code quality
- Individual developers needing structured development workflows

---

## Example Prompts

- `/nflow-init` — Initialize new project
- `/nflow-requirements` — Define product requirements
- `/nflow-plan` — Plan Sprint
- `/nflow-dev` — Start development loop
- `/nflow-review` — Sprint retrospective

---

## Skill Structure

```
nflow/
├── SKILL.md                      # Skill entry point
├── README.md                     # This file
├── commands/                     # 15 command files
│   ├── nflow-init.md           # Project initialization
│   ├── nflow-requirements.md   # Requirements definition
│   ├── nflow-design.md         # Design system
│   ├── nflow-prototype.md      # Prototype design
│   ├── nflow-plan.md           # Sprint planning
│   ├── nflow-dev.md            # Development loop (entry)
│   ├── nflow-dev-workflow.md   # Workflow details
│   ├── nflow-dev-tdd.md        # TDD flow
│   ├── nflow-dev-e2e.md        # E2E testing
│   ├── nflow-dev-review.md     # Code review
│   ├── nflow-resume.md         # Resume development
│   ├── nflow-story.md          # Single Story
│   ├── nflow-review.md         # Final review
│   ├── nflow-new-spec.md       # New requirements handling
│   └── nflow-hotfix-planning.md # Hotfix sprint planning
│
├── agents/                      # 16 Agent personas
│   ├── 01-lead-agent.md
│   ├── 02-pm-agent.md
│   ├── 03-architect-agent.md
│   ├── 04-developer-agent.md
│   ├── 05-techlead-agent.md
│   ├── 06-qa-agent.md
│   ├── 07-scrummaster-agent.md
│   ├── 08-analyst-agent.md
│   └── 00-*-agent.md (8 specialized agents)
│
├── references/                 # Knowledge base (lazy-loaded)
│   ├── tdd-rules.md           # TDD methodology
│   ├── git-worktree.md        # Git worktree guide
│   ├── code-review.md          # Code review standards
│   ├── e2e-testing.md        # E2E testing guide
│   ├── sprint-planning.md      # Sprint planning guide
│   ├── requirements.md         # Requirements gathering
│   ├── design-system.md        # Design system guide
│   ├── prototype.md            # Prototype guide
│   ├── change-control.md       # Change control gate
│   └── memory-management.md    # Memory management
│
├── templates/                   # Template files
│   ├── project-memory.md        # Project memory
│   ├── decision-log.md          # Decision log
│   ├── sprint-review.md         # Sprint retrospective
│   └── ...
│
└── scripts/                    # Utility scripts
    ├── install-openclaw.sh
    ├── install-claude-code.sh
    ├── install-codex.sh
    ├── nflow_tools.py          # State management
    └── spawn-dev-agent.py      # External Agent launcher
```

---

## Quick Install

### OpenClaw

```bash
# Global install
./scripts/install-openclaw.sh --mode agent

# Activate skill
/nflow
```

### Claude Code

```bash
# Install to project directory
./scripts/install-claude-code.sh --local /path/to/project

# Use commands directly
/nflow-init
```

### Codex

```bash
# Install
./scripts/install-codex.sh --local /path/to/project
```

---

## Lazy-Loading Design

NFlow uses lazy-loading to optimize token usage:

### Principle

```
Before: Load ALL knowledge upfront → waste tokens
After:  Load knowledge WHEN needed → efficient
```

### How It Works

| Step | Loaded |
|------|--------|
| Start `/nflow-dev` | Entry file (~400 tokens) |
| Begin TDD | `references/tdd-rules.md` |
| Begin E2E | `references/e2e-testing.md` |
| Begin Review | `references/code-review.md` |

### Knowledge Base

The `references/` directory contains modular knowledge:
- `tdd-rules.md` - TDD methodology
- `git-worktree.md` - Git operations
- `code-review.md` - Review standards
- `e2e-testing.md` - E2E testing
- `sprint-planning.md` - Sprint planning
- etc.

Commands reference these files only when needed.

---

## Workflow Overview

| Phase | Command | Description |
|-------|---------|-------------|
| 0 | `/nflow-init` | Project initialization |
| 1 | `/nflow-requirements` | Market research → PRD → Architecture |
| 2-3 | `/nflow-design` | Design system + Wireframes |
| 4-5 | `/nflow-prototype` | Prototype + Human review |
| 6-7 | `/nflow-plan` | Backlog + Sprint planning |
| 8 | `/nflow-dev` | Development loop |
| 9 | `/nflow-review` | Final review |

---

## Features

### TDD Development Loop
```
8.5 TDD Development ←→ 8.8 Testing
          ↓
     RED → GREEN → REFACTOR
```

### 3-Strike Rules
- Test fails 3 times → Human intervention
- Review fails 3 times → Human intervention

### Git Worktree Isolation
Each Story develops in an isolated worktree, no interference.

### E2E Testing with Screenshots
- Each test step is captured as screenshot
- Filename format: `us{id}-case{id}-step{n}.png`
- Auto-generated HTML acceptance report with all screenshots

### Sprint Review HTML Report
- Auto-generated `review-report.html` for each Sprint
- Includes metrics, retrospective, quality checks, and next steps

### Memory Management
- `project-memory.md` — Global project memory
- `decision-log.md` — Decision audit trail
- `sprint-*/review.md` — Sprint retrospectives

---

## License

MIT
