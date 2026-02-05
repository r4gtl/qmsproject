# Commands — QMSProject

## Docker

- Start dev: `docker compose up -d --build`
- Logs: `docker compose logs -f <service>`

## Backend (Django)

- Migrations: `python manage.py makemigrations` / `python manage.py migrate`
- Tests: `python manage.py test`
- Shell: `python manage.py shell`

## Frontend (Vite)

- Install: `npm ci` (or `npm install`)
- Dev: `npm run dev`
- Build: `npm run build`
- Lint: `npm run lint` (if configured)
