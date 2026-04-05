# Prototype Design

## Phase 5 Output

| Document | Purpose |
|----------|---------|
| mockups/*.html | Interactive prototypes |

---

## Mockup Structure

```
mockups/
├── index.html          # Main prototype
├── css/
│   └── style.css      # Styles
├── js/
│   └── app.js         # Interactions
└── assets/
    └── images/        # Images
```

---

## Interactive Elements

### Form Elements

```html
<input type="text" placeholder="Enter name">
<input type="email" placeholder="Enter email">
<input type="password" placeholder="Enter password">
<button type="submit">Submit</button>
```

### Navigation

```html
<nav>
  <a href="#home">Home</a>
  <a href="#about">About</a>
  <a href="#contact">Contact</a>
</nav>
```

### Cards

```html
<div class="card">
  <img src="image.jpg" alt="Title">
  <h3>Card Title</h3>
  <p>Card description</p>
  <button>Action</button>
</div>
```

---

## Prototype Requirements

| Requirement | Description |
|-------------|-------------|
| Clickable | All links and buttons work |
| Responsive | Works on mobile |
| Accessible | Screen reader friendly |
| Fast | Loads < 3 seconds |

---

## HTML Best Practices

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <!-- Content -->
  <script src="app.js"></script>
</body>
</html>
```

---

## Usability Checklist

- [ ] Clear navigation
- [ ] Consistent design
- [ ] Error handling
- [ ] Loading states
- [ ] Empty states
- [ ] Responsive design
