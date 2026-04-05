# Git Worktree Management

## Why Worktree

- Each Story develops in ISOLATED branch
- No interference between Stories
- Easy to switch context
- Parallel development

---

## Commands

### Create Worktree

```bash
git worktree add ../worktrees/story-{id}-{name} feat/story-{id}
```

### List Worktrees

```bash
git worktree list
```

### Remove Worktree

```bash
git worktree remove ../worktrees/story-{id}-{name}
```

---

## Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feat/story-{id}` | `feat/story-001` |
| Bugfix | `fix/story-{id}` | `fix/story-001` |
| Hotfix | `hotfix/{issue-id}` | `hotfix/HOTFIX-001` |

---

## Commit Rules

- Atomic commits (one logical change per commit)
- Clear commit message
- Reference Story ID in message

### Commit Message Format

```
{type}: {short description}

{long description if needed}

Refs: STORY-001
```

---

## Merge Strategy

1. Complete Story development
2. Run all tests
3. Merge to main via PR
4. Delete worktree after merge

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Worktree conflict | Remove old worktree first |
| Uncommitted changes | Commit or stash before creating worktree |
| Branch exists | Use `-B` to force create |

---

## Worktree Cleanup

```bash
# List all worktrees
git worktree list

# Remove completed worktree
git worktree remove ../worktrees/story-001-user-register
git branch -d feat/story-001
```
