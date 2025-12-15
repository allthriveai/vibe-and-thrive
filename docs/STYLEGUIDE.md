# Why You Need an HTML Styleguide

An HTML styleguide is one of the most powerful tools for AI-assisted coding. It's a living reference that shows AI exactly what your UI should look like.

## What is an HTML Styleguide?

A styleguide is a single HTML page (or route in your app) that displays all your UI components in one place:

- Buttons (all variants, sizes, states)
- Form inputs (text, select, checkbox, etc.)
- Cards, modals, alerts
- Typography (headings, body, links)
- Colors, spacing, shadows
- Layout patterns

**Example route:** `/styleguide` or `/styleguide-neon`

## Why AI Needs a Styleguide

### 1. AI Can't See Your Design

When you say "make a button," AI doesn't know:
- Your brand colors
- Your border radius preferences
- Your hover states
- Your spacing system

Without a styleguide, AI guesses. With one, AI copies.

### 2. Consistency Across Features

Without a styleguide:
```
Feature A: <button class="btn-primary rounded-lg px-4 py-2">
Feature B: <button class="button blue rounded px-3 py-1">
Feature C: <button style="background: blue; padding: 8px 16px;">
```

With a styleguide:
```
All features: <Button variant="primary">
```

### 3. Faster Development

Instead of:
> "Make a card with a shadow, rounded corners, white background,
> padding of 24px, and a subtle border..."

You say:
> "Use our Card component from the styleguide"

### 4. AI Learns Your Patterns

When AI reads your styleguide, it learns:
- Your naming conventions
- Your component API
- Your design tokens
- Your accessibility patterns

## What to Include

### Essential Components

```
/styleguide
├── Colors
│   ├── Primary, Secondary, Accent
│   ├── Success, Warning, Error
│   └── Neutrals (gray scale)
├── Typography
│   ├── Headings (h1-h6)
│   ├── Body text (sizes)
│   └── Links, labels, captions
├── Buttons
│   ├── Variants (primary, secondary, ghost)
│   ├── Sizes (sm, md, lg)
│   └── States (hover, active, disabled, loading)
├── Forms
│   ├── Text inputs
│   ├── Selects
│   ├── Checkboxes, radios
│   ├── Validation states
│   └── Form layouts
├── Cards
│   ├── Basic card
│   ├── Card with header
│   └── Interactive cards
├── Feedback
│   ├── Alerts/toasts
│   ├── Modals
│   └── Loading states
└── Layout
    ├── Containers
    ├── Grids
    └── Spacing examples
```

### Show All States

For each component, show:
- Default state
- Hover state
- Active/pressed state
- Focus state (accessibility!)
- Disabled state
- Loading state (if applicable)
- Error state (for forms)

### Include Code Snippets

Show the code alongside the component:

```html
<!-- Primary Button -->
<Button variant="primary" size="md">
  Click me
</Button>

<!-- With loading state -->
<Button variant="primary" loading>
  Saving...
</Button>
```

## How to Reference in Prompts

### Basic Reference
```
Build the checkout form. Use the /styleguide for component styles.
```

### Specific Components
```
Create a user profile card using the Card and Avatar components
from /styleguide. Match the spacing and typography.
```

### Design System
```
Build this feature following our design system in /styleguide-neon.
Use the neon glass aesthetic with the glow effects shown there.
```

### New Component
```
I need a new Tooltip component. Look at the existing components in
/styleguide for patterns (naming, props API, styling approach) and
create something consistent.
```

## Building Your Styleguide

### Option 1: Dedicated Route (Recommended)

```tsx
// src/pages/Styleguide.tsx
export default function Styleguide() {
  return (
    <div className="p-8 space-y-12">
      <section>
        <h2>Colors</h2>
        <div className="flex gap-4">
          <div className="w-20 h-20 bg-primary rounded" />
          <div className="w-20 h-20 bg-secondary rounded" />
          {/* ... */}
        </div>
      </section>

      <section>
        <h2>Buttons</h2>
        <div className="flex gap-4">
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="ghost">Ghost</Button>
        </div>
      </section>

      {/* ... more sections */}
    </div>
  );
}
```

### Option 2: Storybook

If you use Storybook, it already serves as a styleguide. Reference it:
```
Check our Storybook at localhost:6006 for component patterns.
```

### Option 3: Static HTML File

For simple projects, a single HTML file works:
```html
<!-- styleguide.html -->
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <h1>Styleguide</h1>

  <section id="buttons">
    <h2>Buttons</h2>
    <button class="btn-primary">Primary</button>
    <button class="btn-secondary">Secondary</button>
  </section>

  <!-- ... -->
</body>
</html>
```

## Styleguide as CLAUDE.md

You can also document your design system in CLAUDE.md:

```markdown
## Design System

### Colors
- Primary: #6366f1 (indigo-500)
- Secondary: #8b5cf6 (violet-500)
- Background: #0f0f0f
- Surface: #1a1a1a

### Components
Always use components from @/components/ui:
- Button: variants (primary, secondary, ghost), sizes (sm, md, lg)
- Input: includes label, error state, helper text
- Card: use for content containers

### Patterns
- Use 8px spacing grid (p-2, p-4, p-6, p-8)
- Border radius: rounded-lg for cards, rounded-md for buttons
- Shadows: shadow-lg for elevated elements
```

## Real Example: Neon Glass Styleguide

```tsx
// /styleguide-neon - A themed styleguide
export default function NeonStyleguide() {
  return (
    <div className="min-h-screen bg-black text-white p-8">
      <h1 className="text-4xl font-bold mb-8
        text-transparent bg-clip-text
        bg-gradient-to-r from-cyan-400 to-purple-500">
        Neon Glass Design System
      </h1>

      {/* Glass Card */}
      <section className="mb-12">
        <h2 className="text-xl mb-4 text-cyan-400">Cards</h2>
        <div className="p-6 rounded-xl
          bg-white/5 backdrop-blur-xl
          border border-white/10
          shadow-[0_0_30px_rgba(0,255,255,0.1)]">
          <h3>Glass Card</h3>
          <p className="text-gray-400">
            Frosted glass effect with subtle glow
          </p>
        </div>
      </section>

      {/* Neon Buttons */}
      <section className="mb-12">
        <h2 className="text-xl mb-4 text-cyan-400">Buttons</h2>
        <div className="flex gap-4">
          <button className="px-6 py-2 rounded-lg
            bg-cyan-500 text-black font-semibold
            shadow-[0_0_20px_rgba(0,255,255,0.5)]
            hover:shadow-[0_0_30px_rgba(0,255,255,0.8)]
            transition-shadow">
            Neon Primary
          </button>
          <button className="px-6 py-2 rounded-lg
            border border-cyan-500 text-cyan-400
            hover:bg-cyan-500/10
            transition-colors">
            Neon Ghost
          </button>
        </div>
      </section>

      {/* ... more neon components */}
    </div>
  );
}
```

## Maintenance Tips

### Keep It Updated
When you add new components, add them to the styleguide. Make it part of your PR checklist.

### Make It Accessible
Your styleguide should be easy to find:
- Link in README
- Link in CLAUDE.md
- Bookmark in your browser

### Test Components There
Use the styleguide to visually test components in isolation before using them in features.

### Version It
If your design system evolves, keep notes on what changed and when.

## The ROI

Time spent creating styleguide: **2-4 hours**

Time saved per feature: **30-60 minutes**

After 5-10 features, the styleguide has paid for itself. Plus:
- More consistent UI
- Faster onboarding for new devs
- AI generates better code
- Easier design reviews

## Quick Start

1. Create `/styleguide` route
2. Add your existing components
3. Show all variants and states
4. Reference it in prompts: "Use /styleguide for styles"
5. Keep it updated as you build

Or use the `/styleguide` slash command to generate one interactively!

## Resources

### Component Libraries

- **[21st.dev](https://21st.dev/)** - AI-friendly React components built with Tailwind. Great starting point for your styleguide.
- **[shadcn/ui](https://ui.shadcn.com/)** - Copy-paste components for React
- **[Tailwind UI](https://tailwindui.com/)** - Official Tailwind components
- **[Radix UI](https://www.radix-ui.com/)** - Unstyled, accessible primitives

### Design Inspiration

- **[Dribbble](https://dribbble.com/)** - UI design inspiration
- **[Mobbin](https://mobbin.com/)** - Real app UI patterns
- **[Refero](https://refero.design/)** - Web design references

---

## See Also

- [PROMPTS.md](PROMPTS.md) - How to reference styleguide in prompts
- [BAD-PATTERNS.md](BAD-PATTERNS.md) - Inconsistent styling patterns to avoid
