# Frontend Patterns — React + TS + React-Bootstrap (QMSProject)

## Golden files (reference examples)

### Router entry
**File**: `frontend/src/App.tsx:1-439`
- React Router v6 with `<Routes>` and `<Route>`
- PrivateRoute wrapper + Layout component per ogni route autenticata
- Pattern: `<Route path="/path" element={<PrivateRoute><Layout><Component /></Layout></PrivateRoute>} />`
- Navigate redirect: `<Route path="/" element={<Navigate to="/dashboard" />} />`
- ToastContainer in App root (position="top-right", autoClose=3000)

### Sidebar contextual logic
**File**: `frontend/src/components/layout/Sidebar.tsx:1-93`
- Offcanvas Bootstrap component
- `useLocation()` per pathname detection
- `isInAcquistoPelli = location.pathname.startsWith('/acquistopelli')`
- Conditional sections: `{isInAcquistoPelli && <> ... </>}`
- Nav.Link as={Link} to="/path" onClick={onHide}

### Breadcrumbs with dynamic labels
**File**: `frontend/src/components/layout/Breadcrumbs.tsx:1-278`
- breadcrumbNameMap (static routes)
- `matchPath({ path: pattern, end: true }, pathname)` per route dinamiche
- useEffect + axios per caricare label entity (es: fornitore.ragionesociale)
- Custom logic per nested routes (es: articolo → procedura)
- Breadcrumb.Item linkAs={Link} linkProps={{ to: path }}

### Table-with-actions page (list + filter + pagination)
**File**: `frontend/src/apps/human-resources/pages/EmployeesPage.tsx:1-150`
- useState per dipendenti, loading, searchQuery, page
- useDebounce hook (300ms) per search input
- useCallback per fetchDipendenti con params: { page, page_size, q }
- PaginatedResponse<T> type con count/next/previous/results
- Table con righe cliccabili (onClick -> navigate)
- Azioni: delete con e.stopPropagation() + confirm()
- Toast success/error
- Badge per count, Spinner per loading

### Generic tables cards page (multi-table CRUD)
**File**: `frontend/src/apps/acquistopelli/pages/TabelleGenerichePage.tsx:1-120`
- Container con Row/Col grid (6 card su 2 colonne)
- Card con fixed height (500px) + overflowY auto (420px)
- GenericTableCard<T> component riutilizzabile
- Props: columns, fetchFn, createFn, updateFn, deleteFn, formFields, searchKey
- React-icons per icone header (FaPaw, FaScroll, FaStar, etc.)

### Axios instance + JWT refresh interceptor
**File**: `frontend/src/api/axios.ts:1-59`
- axios.create con baseURL da env (VITE_API_BASE_URL)
- Request interceptor: aggiunge `Authorization: Bearer ${token}` da localStorage
- Response interceptor: su 401 tenta refresh via `/token/refresh/`
- Se refresh fallisce: clear localStorage + redirect a /login
- originalRequest._retry flag per evitare loop

### Auth context
**File**: `frontend/src/context/AuthContext.tsx:1-81`
- createContext + useContext hook pattern
- State: user (User | null), isAuthenticated (boolean)
- login(): POST /token/, salva access+refresh in localStorage, fetchCurrentUser()
- logout(): clear localStorage + navigate('/login')
- useEffect: carica user se accessToken presente al mount
- AuthProvider wraps app tree

## Standard list page pattern

**Structure** (vedi EmployeesPage.tsx per esempio completo):
```tsx
- useState: items[], loading, searchQuery, page, totalCount, next/prev
- useDebounce(searchQuery, 300)
- useCallback fetchItems() con params { page, page_size, q }
- useEffect(() => fetchItems(), [fetchItems])
- useEffect(() => setPage(1), [debouncedSearch]) // reset page on search
- handleRowClick(id) -> navigate(`/path/${id}`)
- handleDelete(e, id) -> e.stopPropagation() + confirm() + delete + toast
- Table con Badge count, Spinner loading, pulsante "Aggiungi"
```

**Pagination**: Backend DRF PageNumberPagination (PAGE_SIZE=50), frontend usa next/previous/count

## Forms

- React-Bootstrap form controls
- Minimal validation on client, rely on backend validation too
- On create success: navigate to edit route

## Nested tables in forms

- Only show nested sections after parent entity has an `id`
- CRUD nested rows via dedicated endpoints or nested payload (match backend design)
