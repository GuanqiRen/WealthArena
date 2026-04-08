# WealthArena Frontend (Phase 7)

Read-only web dashboard built with Next.js App Router and TypeScript.

## Routes

- /login
- /dashboard
- /portfolio/[id]

## Features

- JWT login against backend /auth/login
- Google OAuth login via Supabase
- Protected routes (all except /login)
- Portfolio listing
- Position table
- Trade history table
- Basic portfolio summary (position count and gross exposure)

## Setup

1. Install dependencies:

   npm install

2. Configure API base URL:

   cp .env.local.example .env.local

   Fill in the Supabase variables for Google OAuth:

   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_PUBLIC_KEY=your_supabase_public_key

3. Start app:

   npm run dev

   The dev server is configured to bind to 0.0.0.0:3000, so you can access it via localhost or your LAN IP.

4. Open:

   http://localhost:3000

## If You See ChunkLoadError

If you see an error like `ChunkLoadError: Loading chunk app/login/page failed`, use this quick reset:

1. Stop the dev server.
2. Remove Next cache:

   rm -rf .next

3. Start again:

   npm run dev

4. Hard refresh your browser (or open a new private window).

## Backend Requirement

Backend API should be running at NEXT_PUBLIC_API_BASE_URL (default: http://localhost:8000).
