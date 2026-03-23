# WealthArena Frontend (Phase 7)

Read-only web dashboard built with Next.js App Router and TypeScript.

## Routes

- /login
- /dashboard
- /portfolio/[id]

## Features

- JWT login against backend /auth/login
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

3. Start app:

   npm run dev

4. Open:

   http://localhost:3000

## Backend Requirement

Backend API should be running at NEXT_PUBLIC_API_BASE_URL (default: http://localhost:8000).
