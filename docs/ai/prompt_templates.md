# Prompt Templates — Sonnet-friendly (QMSProject)

## Template A — Discovery (fill TODO in docs/ai)

Goal: locate the real reference files and conventions in this repo.
Task:

- Find router entry, sidebar contextual logic, breadcrumbs, axios instance, auth context/interceptor.
- Find backend DRF patterns: a CRUD viewset, filtered list viewset, router registration, pagination/permissions defaults.
- Update:
  - @docs/ai/project_context.md
  - @docs/ai/patterns_backend.md
  - @docs/ai/patterns_frontend.md
    Output:
- Unified diff only.
  Rules:
- No implementation of new features.
- Keep notes concise.

## Template B — Backend slice

Context:
@docs/ai/project_context.md
@docs/ai/patterns_backend.md
@docs/ai/<feature>\_spec.md

Task:

- Implement ONLY: <scope>
- Touch ONLY: <file list>
- Optimize queries (select_related/prefetch_related)
- Output: unified diff + migration diff (if created)
  Fail-fast:
- If db_table decision is required, stop and ask for the exact command output to decide.

## Template C — Frontend slice

Context:
@docs/ai/project_context.md
@docs/ai/patterns_frontend.md
@docs/ai/<feature>\_spec.md

Task:

- Implement ONLY: <scope>
- Touch ONLY: <file list>
- Reuse existing components (toasts/modals/confirm)
- Output: unified diff
  Fail-fast:
- If a reference pattern file is missing, stop and ask which existing page to mimic.
