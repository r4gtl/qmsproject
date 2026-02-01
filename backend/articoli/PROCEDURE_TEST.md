# Test e Deploy - Sistema Procedure

## Logica Numerazione

| Scenario | nr_procedura | nr_revisione |
|----------|--------------|--------------|
| Prima procedura per articolo X | `nextval(sequence)` | 1 |
| Seconda procedura per articolo X | stesso della prima | 2 |
| Prima procedura per articolo Y | `nextval(sequence)` (diverso da X) | 1 |

**Regola chiave**: `nr_procedura` identifica la "serie" di un articolo, `nr_revisione` incrementa dentro la serie.

---

## Deploy

```bash
# In ambiente Docker
docker compose exec backend python manage.py migrate

# Verifica sequence sincronizzata
docker compose exec -T backend python manage.py dbshell <<'SQL'
SELECT last_value, is_called FROM procedura_nr_seq;
SQL
```

### Comportamento setval/nextval

La migration usa:

```sql
SELECT setval('procedura_nr_seq', N, false);
```

Dove `N = COALESCE(MAX(nr_procedura), 0) + 1`.

**Semantica `setval(seq, value, is_called)`**:

- `is_called = false`: il prossimo `nextval()` restituirà **esattamente** `value`
- `is_called = true`: il prossimo `nextval()` restituirà `value + 1`

**Expected output dopo migrate** (tabella vuota):

```text
 last_value | is_called
------------+-----------
          1 | f
```

→ prossimo `nextval()` = 1

**Expected output** (se MAX(nr_procedura)=5):

```text
 last_value | is_called
------------+-----------
          6 | f
```

→ prossimo `nextval()` = 6

**Verifica consumando un valore** (opzionale, altera la sequence):

```sql
SELECT nextval('procedura_nr_seq');
-- Restituisce il prossimo nr_procedura disponibile
```

---

## Test Concorrenza

### A) Test revisioni simultanee sullo STESSO articolo

Verifica che 5 creazioni parallele producano:

- **Stesso** `nr_procedura` per tutte
- `nr_revisione` **unici e consecutivi** (1,2,3,4,5 o simili)
- Nessun errore 500

```bash
# Esegui 5 POST simultanei
for i in {1..5}; do
  curl -s -X POST http://localhost:8000/api/articoli/procedure/ \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"fk_articolo": 1}' &
done
wait

# Verifica risultati (compatibile con API paginata e non)
curl -s "http://localhost:8000/api/articoli/procedure/?fk_articolo=1" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '[(.results // .)[] | {id, nr_procedura, nr_revisione}] | sort_by(.nr_revisione)'
```

**Expected output** (esempio):

```json
[
  {"id": 10, "nr_procedura": 3, "nr_revisione": 1},
  {"id": 11, "nr_procedura": 3, "nr_revisione": 2},
  {"id": 12, "nr_procedura": 3, "nr_revisione": 3},
  {"id": 13, "nr_procedura": 3, "nr_revisione": 4},
  {"id": 14, "nr_procedura": 3, "nr_revisione": 5}
]
```

**Validazione nr_procedura unico**:

```bash
# Deve restituire 1 (un solo nr_procedura distinto)
curl -s "http://localhost:8000/api/articoli/procedure/?fk_articolo=1" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '[(.results // .)[].nr_procedura] | unique | length'
```

**Validazione nr_revisione contigui**:

```bash
# Deve restituire true (max - min + 1 == count)
curl -s "http://localhost:8000/api/articoli/procedure/?fk_articolo=1" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '[(.results // .)[].nr_revisione] | unique | (max - min + 1) == length'
```

---

### B) Test nr_procedura DIVERSI per articoli diversi

**Precondizione**: questo test vale solo per articoli **senza procedure pregresse**.
Se un articolo ha già una procedura, il POST crea una nuova revisione (nr_procedura invariato).

**Script completo** (copy-paste safe):

```bash
# Crea 5 articoli e cattura gli ID
ART_IDS=$(for i in {1..5}; do
  curl -s -X POST "http://localhost:8000/api/articoli/articoli/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"descrizione\":\"Test Art $RANDOM\"}" \
  | jq -r '.id'
done)

echo "Articoli creati: $ART_IDS"

# Crea una procedura per ciascun articolo (in parallelo)
for art_id in $ART_IDS; do
  curl -s -X POST "http://localhost:8000/api/articoli/procedure/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"fk_articolo\": $art_id}" >/dev/null &
done
wait

# Verifica: nr_procedura devono essere tutti diversi
curl -s "http://localhost:8000/api/articoli/procedure/" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '(.results // .)
        | map(select(.nr_revisione == 1) | {fk_articolo, nr_procedura})
        | group_by(.nr_procedura)
        | map(select(length > 1))'
```

**Expected output** (nessun duplicato):

```json
[]
```

Se l'output non è vuoto, significa che due articoli diversi hanno lo stesso `nr_procedura` (bug nella sequence).

**Nota**: Se usi articoli con procedure esistenti, vedrai `nr_revisione > 1` e `nr_procedura` uguale alla procedura precedente (comportamento corretto).

---

## Test CRUD Caratteristiche

### Lavorazione INTERNA (is_interna=true)

```bash
# Deve funzionare: solo fk_dettaglio_fase_lavoro
curl -X POST http://localhost:8000/api/articoli/caratteristiche-procedura/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fk_dettaglio_procedura": 1, "fk_dettaglio_fase_lavoro": 5, "valore": "100°C", "numero_riga": 1}'

# Deve FALLIRE: fornitore su lavorazione interna
curl -X POST http://localhost:8000/api/articoli/caratteristiche-procedura/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fk_dettaglio_procedura": 1, "fk_fornitore": 1, "numero_riga": 2}'
# Expected: 400 Bad Request
```

### Lavorazione ESTERNA (is_interna=false)

```bash
# Deve funzionare: fornitore + lavorazione_esterna
curl -X POST http://localhost:8000/api/articoli/caratteristiche-procedura/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fk_dettaglio_procedura": 2, "fk_fornitore": 1, "fk_lavorazione_esterna": 1, "numero_riga": 1}'

# Deve FALLIRE: manca fk_lavorazione_esterna
curl -X POST http://localhost:8000/api/articoli/caratteristiche-procedura/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fk_dettaglio_procedura": 2, "fk_fornitore": 1, "numero_riga": 2}'
# Expected: 400 Bad Request
```

---

## Verifica Constraint DB

```sql
-- Esegui in dbshell (psql)
\d articoli_procedura
-- Deve mostrare: ux_procedura_articolo_nr_rev

\d articoli_dettaglioprocedura
-- Deve mostrare: ux_dettaglio_procedura_riga

\d articoli_caratteristicaprocedura
-- Deve mostrare: ux_caratteristica_procedura_riga

-- Query alternativa (funziona anche in altri client SQL):
SELECT conname, conrelid::regclass AS table_name
FROM pg_constraint
WHERE conname IN (
  'ux_procedura_articolo_nr_rev',
  'ux_dettaglio_procedura_riga',
  'ux_caratteristica_procedura_riga'
);
```

---

## Sequence Postgres

```sql
-- Verifica stato sequence (non consuma valori)
SELECT last_value, is_called FROM procedura_nr_seq;

-- Interpretazione:
-- is_called=f → nextval() restituirà last_value
-- is_called=t → nextval() restituirà last_value + 1

-- Reset manuale (SOLO se necessario)
SELECT setval('procedura_nr_seq',
  COALESCE((SELECT MAX(nr_procedura) FROM articoli_procedura), 0) + 1,
  false
);
```
