# Project Context — QMSProject

## Repo layout

- Backend root: `qmsproject/backend/`
- Frontend root: `qmsproject/frontend/`
- Context packs: `qmsproject/docs/ai/`

## Backend (Django + DRF)

### Where things live

- Project settings: `backend/qmsproject/settings.py`
- Main urls: `backend/qmsproject/urls.py`
- App APIs: `backend/<app>/api.py` (ViewSets) + `backend/<app>/api_urls.py` (router)
- Legacy views: `backend/<app>/views.py` (Django template views)

### Standards (DRF settings.py:328-339)

- Pagination: `PageNumberPagination` (PAGE_SIZE=50)
- Auth: JWT via `rest_framework_simplejwt` (8h access, 7d refresh)
- Default filters: `DjangoFilterBackend`, `OrderingFilter`, `SearchFilter`
- Permissions: **NOT globally set** → ViewSets use `[IsAuthenticated]` per-class

### Golden reference files

- **Simple CRUD ViewSet**: `backend/acquistopelli/api.py:25-50` (TipoAnimaleViewSet)
  - ModelViewSet, SearchFilter/OrderingFilter, perform_create con created_by
- **Filtered list with FK filters**: `backend/acquistopelli/api.py:98-114` (NazioneViewSet)
  - select_related per FK, filterset_fields per dropdown, search_fields multipli
- **Multi-serializer + prefetch**: `backend/acquistopelli/api.py:121-160` (LottoViewSet)
  - get_serializer_class (List/Detail/Write), get_queryset con prefetch_related per retrieve
- **Custom Q filters**: `backend/human_resources/api.py:64-136` (HumanResourceViewSet)
  - Q(nome|cognome) via query param 'q', override create/update per ritornare detail serializer
- **Router registration**: `backend/human_resources/api_urls.py:34-76`
  - DefaultRouter, basename custom, urlpatterns = router.urls

## Frontend (React + TS + Vite)

### Where things live

- Router entry: `frontend/src/App.tsx` (React Router v6, PrivateRoute wrapper)
- Layout & sidebar: `frontend/src/components/layout/Layout.tsx` + `Sidebar.tsx` + `Breadcrumbs.tsx`
- Dashboard: `frontend/src/pages/dashboard/Dashboard.tsx`
- App modules: `frontend/src/apps/<appname>/pages/` (es: acquistopelli, human_resources)

### Golden reference files

- **Table-with-actions page**: `frontend/src/apps/human_resources/pages/EmployeesPage.tsx`
  - react-table v8, filtri, azioni edit/delete, modal confirm
- **Generic tables cards page**: `frontend/src/apps/acquistopelli/pages/TabelleGenerichePage.tsx`
  - Card con tab per 3 tabelle, GenericTable component riutilizzabile
- **Sidebar contextual logic**: `frontend/src/components/layout/Sidebar.tsx`
  - useLocation, isInAcquistoPelli = pathname.startsWith('/acquistopelli')
- **Breadcrumbs**: `frontend/src/components/layout/Breadcrumbs.tsx`
  - breadcrumbNameMap con matchPath per path dinamici (/lotti/:id)

## Quick “how we add a new app”

- Backend: create serializers/viewsets + register in app urls/router.
- Frontend: add routes under `/APPNAME`, add contextual sidebar group, add a dashboard card.
