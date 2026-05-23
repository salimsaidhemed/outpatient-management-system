# Outpatient Admissions System

A modern MVP for outpatient front-desk workflows with a Flask REST API, PostgreSQL, Docker Compose, Vue 3, and Vuetify.

## Features

- Patient registration with MRN generation
- Outpatient admission creation
- Admissions queue with discharge action
- Patient visit history
- Dashboard metrics and department load
- Printable admission receipt
- Keycloak authentication

## Project Structure

```text
.
├── backend
│   ├── app
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extensions.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── services
│   │   ├── styles
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── .env.example
```

## Run With Docker Compose

```bash
docker compose up --build
```

If your Docker installation uses the legacy Compose binary:

```bash
docker-compose up --build
```

Then open:

- Frontend: http://localhost:5173
- Backend health check: http://localhost:5050/health
- API base: http://localhost:5050/api
- Keycloak admin: http://localhost:8080

Demo credentials:

- App user: `receptionist` / `receptionist`
- Admin user: `admin.reception` / `admin`
- Keycloak admin: `admin` / `admin`

The backend creates the initial database tables on startup for MVP convenience.

The API requires a Keycloak bearer token for every `/api/*` request. The `outpatient`
realm, `admissions-frontend` public client, demo users, and roles are imported from
`keycloak/realm-export.json` when the Keycloak container starts.

Role model:

- `admissions_user`: access dashboard, register patients, create admissions, view history, and print receipts.
- `admissions_admin`: access admin-only routes and discharge outpatient admissions.

See `docs/access-control.md` for the complete roles and access matrix.

Frontend routes:

- `/`: dashboard
- `/patients/register`: patient registration
- `/admissions/new`: outpatient admission
- `/admissions`: admissions queue
- `/patients/history`: visit history
- `/admin`: admin-only workspace

## API Endpoints

- `GET /api/dashboard`
- `GET /api/patients?q=`
- `POST /api/patients`
- `GET /api/patients/<patient_id>`
- `GET /api/admissions`
- `POST /api/admissions`
- `PATCH /api/admissions/<admission_id>/discharge`
- `GET /api/admissions/<admission_id>/receipt`

## Suggested Next Steps

- Add Alembic migrations
- Add authentication and role-based access
- Add insurance details and billing workflow
- Add appointment scheduling
- Add automated backend and frontend test suites
