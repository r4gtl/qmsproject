# Backend Patterns — Django + DRF (QMSProject)

## Golden files (fill during discovery)

- CRUD ViewSet example: TODO
- Filtered/paginated list example: TODO
- Nested detail + prefetch example: TODO
- Existing router registration example: TODO

## Default ViewSet pattern (expected)

- `ModelViewSet`
- `permission_classes = [IsAuthenticated]` (unless project differs)
- `filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]`
- `search_fields = [...]` (icontains on name/descrizione)
- `ordering_fields = [...]`
- `ordering = [...]` (sensible default)

## Query optimization rules

- Use `select_related()` for FKs used in serializers.
- Use `prefetch_related()` for reverse FK / M2M lists.
- Avoid returning huge nested structures in list endpoints.

## Serializer rules

- List serializer should include human-readable labels (e.g., supplier name) to avoid extra calls.
- Detail serializer may include nested lists (scelte/origini), but keep it controlled.

## Legacy tables / db_table

If mapping existing DB tables (e.g., imported from Access):

- Use `class Meta: db_table = "..."`.
- Avoid migrations that attempt to create/drop/rename those tables unless explicitly requested.
- Prefer constraints/indexes only if safe and requested.
