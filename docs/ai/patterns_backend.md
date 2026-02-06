# Backend Patterns — Django + DRF (QMSProject)

## Golden files (reference examples)

### Simple CRUD ViewSet
**File**: `backend/acquistopelli/api.py:25-50` (TipoAnimaleViewSet)
- ModelViewSet base
- SearchFilter + OrderingFilter
- perform_create sets created_by=request.user
- No filterset_fields (simple list)

### Filtered list with FK filters
**File**: `backend/acquistopelli/api.py:98-114` (NazioneViewSet)
- select_related("regione", "subregione") for FK optimization
- filterset_fields=["regione", "subregione"] for dropdowns
- search_fields=["descrizione", "sigla", "sigla_estesa"] (icontains)
- ordering=["descrizione"]

### Multi-serializer + prefetch (list/detail/write)
**File**: `backend/acquistopelli/api.py:121-160` (LottoViewSet)
- get_serializer_class() returns different serializers per action
- get_queryset() uses select_related for FKs, prefetch_related for reverse FKs (only on retrieve)
- ordering=["-data_acquisto"] (most recent first)
- filterset_fields for related entities

### Custom Q filters (search across multiple fields)
**File**: `backend/human_resources/api.py:64-136` (HumanResourceViewSet)
- get_queryset() reads query param 'q' and filters Q(nome__icontains) | Q(cognome__icontains)
- Override create/update to return detail serializer (not write serializer)
- ordering=["-dataassunzione"] (most recent hire first)

### Router registration
**File**: `backend/human_resources/api_urls.py:34-76`
- DefaultRouter() instance
- router.register(r"dipendenti", HumanResourceViewSet, basename="dipendente")
- urlpatterns = router.urls (no path() needed)
- Include in main urls.py: `path("api/human-resources/", include("human_resources.api_urls"))`

## Default ViewSet pattern

**Standard structure** (used across acquistopelli, human_resources, anagrafiche):
```python
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()  # or .select_related(...) if FKs
    serializer_class = MyModelSerializer
    permission_classes = [IsAuthenticated]  # ALWAYS explicit (not in global settings)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["fk_field"]  # Optional: for dropdown filters
    search_fields = ["name", "descrizione"]  # Optional: icontains search
    ordering_fields = ["name", "created_at"]  # Optional: sortable columns
    ordering = ["name"]  # Default sort

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
```

**Pagination/Filters**: Global defaults in `settings.py:328-339`:
- PageNumberPagination (PAGE_SIZE=50)
- DjangoFilterBackend, OrderingFilter, SearchFilter

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
