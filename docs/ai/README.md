# AI Context Packs (QMSProject)

Scopo: evitare prompt giganteschi. Le regole globali stanno in `CLAUDE.md`.
I dettagli si caricano “on demand” con `@docs/ai/<file>.md`.

## Files

- project_context.md: mappa repo + punti di riferimento (router/sidebar, axios, DRF patterns)
- patterns_backend.md: pattern DRF/Django + file “golden” da copiare
- patterns_frontend.md: pattern React + file “golden” da copiare
- commands.md: comandi standard (docker, migrate, build)
- prompt_templates.md: template prompt “Sonnet-friendly”
- \*\_spec.md: specifiche feature/app (es: acquistopelli_spec.md)

## Regola pratica

- Tenere questi file concisi.
- Le specifiche lunghe vanno in un \*\_spec.md dedicato e si richiamano solo quando serve.
