# Frontend Patterns — React + TS + React-Bootstrap (QMSProject)

## Golden files (fill during discovery)

- Table-with-actions page (EmployeesPage-like): TODO
- Generic tables cards page (TabelleGenerichePage-like): TODO
- Router entry file: TODO
- Sidebar contextual logic file: TODO
- Breadcrumbs component usage: TODO
- Toast & confirm modal components: TODO
- Axios instance file: TODO
- Auth context / refresh interceptor: TODO

## Standard list page

- Server-side pagination + filters + ordering
- Debounce inputs 300–500ms
- Row click -> edit route
- Actions: edit/delete with confirm
- Toast success/error

## Forms

- React-Bootstrap form controls
- Minimal validation on client, rely on backend validation too
- On create success: navigate to edit route

## Nested tables in forms

- Only show nested sections after parent entity has an `id`
- CRUD nested rows via dedicated endpoints or nested payload (match backend design)
