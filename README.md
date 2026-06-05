# DevPaste 🚀

**Professional Code Snippet Manager** — Share code snippets instantly with syntax highlighting, expiration, and more.

## Features

- ✅ Create pastes with title, language, expiry, and visibility
- ✅ Auto-generated short slugs
- ✅ Syntax highlighting via highlight.js (atom-one-dark theme)
- ✅ Public & Unlisted visibility
- ✅ View count per paste
- ✅ Paste deletion via secure delete token
- ✅ Raw plaintext view (`/raw/<slug>`)
- ✅ Explore page: browse & search public pastes
- ✅ Auto-expiry (1h / 1d / 7d / 30d / never)
- ✅ Light / Dark theme toggle
- ✅ Responsive mobile-first design
- ✅ Ad slot placeholders (sidebar & below content)
- ✅ Vercel-ready deployment

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python Flask 3.x |
| Database | Supabase (PostgreSQL) |
| Frontend | Jinja2 + Bootstrap 5 + custom CSS |
| Fonts | Space Grotesk + JetBrains Mono |
| Syntax Highlight | highlight.js (atom-one-dark) |
| Deploy | Vercel |

## Setup

### 1. Clone & install dependencies

```bash
git clone <repo-url>
cd DevPaste
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 3. Create Supabase table

Run this SQL in your Supabase SQL editor:

```sql
CREATE TABLE IF NOT EXISTS pastes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,
  title TEXT,
  content TEXT NOT NULL,
  language TEXT NOT NULL DEFAULT 'plaintext',
  visibility TEXT NOT NULL DEFAULT 'public' CHECK (visibility IN ('public', 'unlisted')),
  delete_token TEXT NOT NULL,
  views INTEGER NOT NULL DEFAULT 0,
  expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for fast slug lookups
CREATE INDEX IF NOT EXISTS idx_pastes_slug ON pastes(slug);

-- Index for explore page
CREATE INDEX IF NOT EXISTS idx_pastes_visibility_created ON pastes(visibility, created_at DESC);
```

### 4. Run locally

```bash
python -m flask --app api.index run --debug
# or
gunicorn api.index:app
```

Open [http://localhost:5000](http://localhost:5000)

## Deploy to Vercel

### Prerequisites
- Vercel CLI: `npm i -g vercel`

### Steps

```bash
# Set environment secrets
vercel secrets add supabase_url "https://your-project.supabase.co"
vercel secrets add supabase_key "your-supabase-key"
vercel secrets add secret_key "$(openssl rand -hex 32)"

# Deploy
vercel --prod
```

## Project Structure

```
DevPaste/
├── api/
│   └── index.py         # Vercel entry point
├── app/
│   ├── __init__.py      # Flask app factory + Supabase client
│   ├── routes.py        # URL routes and view handlers
│   ├── models.py        # Supabase query functions
│   └── utils.py         # Slug/token generation, expiry helpers
├── templates/
│   ├── base.html        # Base layout (navbar, footer, toasts)
│   ├── index.html       # New paste form
│   ├── view.html        # Paste viewer with syntax highlight
│   ├── explore.html     # Public paste explorer
│   └── 404.html         # Error page
├── static/
│   ├── css/style.css    # Custom styling (dark/light theme)
│   └── js/main.js       # Theme toggle, clipboard, toasts
├── .env.example
├── requirements.txt
├── vercel.json
└── README.md
```

## Ad Slots

Ad slots are pre-placed as `<div class="ad-slot">` elements:
- `.ad-slot-sidebar` — Right sidebar (250px min-height)
- `.ad-slot-below-content` — Below code block (90px)

Integrate any ad network by targeting these divs.

## License

MIT — DevPaste, built for developers.
