# Design System (CV Grader)

## 🎨 Color Palette
Extracted from the reference images (a blend of the minimal file upload UI and the soft, rounded dropdown UI):

- **Background (Page)**: `#F8F9FA` (Soft, neutral off-white/gray)
- **Surface (Cards/Modals)**: `#FFFFFF` (Pure white)
- **Primary / Accent**: `#000000` (Pitch black for high-contrast action buttons) & `#2563EB` (Vibrant blue for upload states and active elements)
- **Text - Primary**: `#111827` (Near black, high readability)
- **Text - Secondary**: `#6B7280` (Cool gray for metadata and borders)
- **Error / Danger**: `#EF4444` (Text/Border) on `#FEE2E2` (Soft background)
- **Success**: `#10B981` (Green for matched skills/high scores)

## 🔤 Typography
- **Headings (Display)**: *Playfair Display* (Serif). Brings an editorial, sophisticated touch to major titles (like "Upload Files").
- **Body & UI**: *Plus Jakarta Sans* or *Inter* (Sans-serif). Clean, geometric, and modern for maximum legibility in forms, dropdowns, and data.

## ✨ Visual Mood & Motifs
- **Corners**: Highly rounded. Cards use `24px` or `2xl` radii. Buttons and badges are pill-shaped (`rounded-full`).
- **Shadows**: Very soft, diffused drop shadows to create a floating effect without harsh borders.
- **Borders**: Subtle `1px` solid borders (`#E5E7EB`) around inner containers, with heavy rounded styling.
- **Overall Feel**: Minimalist, airy, modern, and highly legible. Focus is drawn to the content and primary actions through high contrast (black on white).

---

### Tailwind Config Extension
Here is the proposed configuration to add to our `tailwind.config.ts` in Step 1:

```typescript
theme: {
  extend: {
    colors: {
      background: '#F8F9FA',
      surface: '#FFFFFF',
      primary: '#000000',
      'primary-blue': '#2563EB',
      'text-main': '#111827',
      'text-muted': '#6B7280',
      success: '#10B981',
      error: '#EF4444',
      'error-bg': '#FEE2E2',
    },
    fontFamily: {
      sans: ['var(--font-plus-jakarta)', 'Inter', 'sans-serif'],
      serif: ['var(--font-playfair)', 'serif'],
    },
    borderRadius: {
      '2xl': '1.5rem',
      '3xl': '2rem',
    },
    boxShadow: {
      'soft': '0 10px 40px -10px rgba(0,0,0,0.05)',
      'floating': '0 20px 40px -10px rgba(0,0,0,0.1)',
    }
  }
}
```
