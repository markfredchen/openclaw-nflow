# Design System

## Phase 2 Output

| Document | Purpose |
|----------|---------|
| design-pattern.json | Design patterns |
| wireframes/ | ASCII wireframes |

---

## Design Pattern JSON

```json
{
  "project": "{name}",
  "version": "1.0",
  "patterns": [
    {
      "name": "repository-pattern",
      "description": "Data access abstraction",
      "files": ["src/repositories/*.py"]
    }
  ],
  "components": [
    {
      "name": "Button",
      "states": ["default", "hover", "active", "disabled"],
      "variants": ["primary", "secondary", "danger"]
    }
  ],
  "colors": {
    "primary": "#667eea",
    "secondary": "#764ba2"
  }
}
```

---

## Wireframe Format

```markdown
# Page Name

+------------------------------------------+
|  Header                                  |
+------------------------------------------+
|  Navigation                              |
+------------------------------------------+
|                                          |
|  +--------+  +--------+  +--------+      |
|  | Card 1 |  | Card 2 |  | Card 3 |      |
|  |        |  |        |  |        |      |
|  +--------+  +--------+  +--------+      |
|                                          |
+------------------------------------------+
|  Footer                                  |
+------------------------------------------+
```

---

## Component States

| State | Meaning |
|-------|---------|
| Default | Normal state |
| Hover | Mouse over |
| Active | Being clicked |
| Disabled | Not interactive |
| Loading | Async operation |
| Error | Error state |
| Empty | No data |

---

## Responsive Breakpoints

| Breakpoint | Width | Device |
|------------|-------|--------|
| Mobile | < 768px | Phone |
| Tablet | 768-1024px | Tablet |
| Desktop | > 1024px | Desktop |
| Wide | > 1440px | Large screen |

---

## Typography Scale

| Level | Size | Usage |
|-------|------|-------|
| H1 | 2.5rem | Page titles |
| H2 | 2rem | Section titles |
| H3 | 1.5rem | Subsection |
| Body | 1rem | Paragraphs |
| Small | 0.875rem | Captions |
| Tiny | 0.75rem | Labels |
