# Project Context — QMSProject

## Repo layout

- Backend root: `qmsproject/backend/`
- Frontend root: `qmsproject/frontend/`
- Context packs: `qmsproject/docs/ai/`

## Backend (Django + DRF) — fill during discovery

### Where things live

- Project settings: `backend/<PROJECT_NAME>/settings.py` (TODO: confirm path)
- Main urls: `backend/<PROJECT_NAME>/urls.py` (TODO: confirm path)
- App APIs: typically `backend/<app>/api.py` or `views.py` (TODO: confirm by scanning)

### Standards (confirm from codebase)

- Pagination: project default via DRF settings (TODO: name/class)
- Permissions default: often `IsAuthenticated` (TODO)
- Filters: `django-filter` + DRF Search/Ordering (TODO)

### Golden reference files (to be filled)

- CRUD ViewSet example: TODO
- Filtered list example (server-side): TODO
- Nested detail / prefetch example: TODO

## Frontend (React + TS + Vite) — fill during discovery

### Where things live

- Router entry: `frontend/src/App.tsx` or `frontend/src/router/*` (TODO)
- Layout & sidebar: `frontend/src/components/layout/*` (TODO)
- Toasts/confirm modals: (TODO)
- Axios instance: (TODO)
- Auth context/interceptor: (TODO)

### Golden reference files (to be filled)

- Table-with-actions page (EmployeesPage-like): TODO
- Generic tables cards page (TabelleGenerichePage-like): TODO
- Sidebar contextual logic: TODO
- Breadcrumbs usage: TODO

## Quick “how we add a new app”

- Backend: create serializers/viewsets + register in app urls/router.
- Frontend: add routes under `/APPNAME`, add contextual sidebar group, add a dashboard card.
