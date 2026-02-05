# Claude Code — QMSProject Rules

## Repo layout

- backend/ (Django + DRF)
- frontend/ (React + TS + Vite)
- docs/ai/ (context packs, loaded only when referenced)

## Working style (must)

- Prefer small, incremental changes. Avoid repo-wide refactors unless explicitly requested.
- Always output **unified diff** for every change.
- Keep diffs minimal: change only what is necessary.
- If you need to modify many files, propose a slice plan first (A/B/C…).

## Fail-fast rule

If a critical decision/data is missing (e.g., whether a legacy table already exists in DB, the exact file that defines routing/sidebar, etc.):

- STOP implementation
- Ask for the exact command output you need (or point to the file path to read)
- Then proceed.

## Backend conventions (Django/DRF)

- User FK: always use `from django.conf import settings` and `settings.AUTH_USER_MODEL`.
- Avoid N+1: use `select_related` / `prefetch_related`.
- Follow existing project patterns for:
  - serializers
  - viewsets
  - filters (django-filter + SearchFilter + OrderingFilter)
  - pagination
  - permissions
- Migrations:
  - If a table already exists (legacy/Access import), map with `db_table` and avoid destructive migrations.
  - Never drop/rename legacy tables unless explicitly requested.

## Frontend conventions (React/TS)

- Use existing axios client with JWT refresh interceptor.
- UI must use React-Bootstrap and project theme.
- Lists: server-side pagination/filtering/sorting; debounce 300–500ms.
- Reuse existing components/patterns for modals, confirms, toasts, tables-with-actions.
- Sidebar is contextual: show app groups only when the current route is inside that app.

## Required output

For any implementation task, return:

1. Unified diff
2. 2–3 minute test checklist (commands + pages/endpoints to verify)

## Context packs (load only when needed)

When a task is app-specific or needs conventions, ask me to include:

- @docs/ai/project_context.md
- @docs/ai/patterns_backend.md
- @docs/ai/patterns_frontend.md
- @docs/ai/commands.md
- @docs/ai/<feature>\_spec.md
