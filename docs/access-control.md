# Roles and Access Matrix

The outpatient admissions system uses Keycloak realm roles for both frontend route access and backend API authorization.

## Where Roles Are Defined

Roles are defined in the Keycloak realm import file:

- `keycloak/realm-export.json`

The imported realm is:

- Realm: `outpatient`
- Client: `admissions-frontend`

Current realm roles:

- `admissions_user`
- `admissions_admin`

Demo users:

| Username | Password | Roles |
| --- | --- | --- |
| `receptionist` | `receptionist` | `admissions_user` |
| `admin.reception` | `admin` | `admissions_user`, `admissions_admin` |

## Role Intent

| Role | Purpose |
| --- | --- |
| `admissions_user` | Standard front-desk role for day-to-day outpatient workflows. |
| `admissions_admin` | Elevated admissions role for restricted operational actions. |

`admissions_admin` is additive. Admin users should usually also have `admissions_user` so they retain normal workflow access.

## Frontend Route Access

Frontend routes are defined in:

- `frontend/src/router/index.js`

The router uses route metadata to decide which roles can access each workspace page. Navigation is also filtered so users only see routes their roles allow.

| Route | Screen | `admissions_user` | `admissions_admin` |
| --- | --- | --- | --- |
| `/` | Dashboard | Yes | Yes |
| `/patients/register` | Register patient | Yes | Yes |
| `/admissions/new` | Admit outpatient | Yes | Yes |
| `/admissions` | Admissions queue | Yes | Yes |
| `/patients/history` | Visit history | Yes | Yes |
| `/admin` | Administration | No | Yes |
| `/access-denied` | Access denied | Yes | Yes |

If a signed-in user opens a route they do not have permission for, the app redirects them to `/access-denied`.

## Backend API Access

Backend authentication and role checks are implemented in:

- `backend/app/auth.py`
- `backend/app/routes.py`

Every `/api/*` route requires a valid Keycloak bearer token. Some routes also require specific roles.

| API | Method | Access |
| --- | --- | --- |
| `/api/dashboard` | `GET` | Any authenticated user |
| `/api/patients` | `GET` | Any authenticated user |
| `/api/patients` | `POST` | `admissions_user` or `admissions_admin` |
| `/api/patients/<patient_id>` | `GET` | Any authenticated user |
| `/api/admissions` | `GET` | Any authenticated user |
| `/api/admissions` | `POST` | `admissions_user` or `admissions_admin` |
| `/api/admissions/<admission_id>/discharge` | `PATCH` | `admissions_admin` only |
| `/api/admissions/<admission_id>/receipt` | `GET` | Any authenticated user |

## Enforcement Notes

- The frontend improves user experience by hiding disallowed navigation and redirecting blocked routes.
- The backend is the source of truth for protected actions.
- CORS preflight `OPTIONS` requests are allowed through before token checks so browser requests can complete correctly.
- Tokens are validated against the Keycloak JWKS endpoint and issuer configured by environment variables.

## Local Development

Start the stack:

```bash
docker-compose up --build
```

Useful URLs:

- App: http://localhost:5173
- API: http://localhost:5050/api
- Keycloak: http://localhost:8080

Keycloak admin:

- Username: `admin`
- Password: `admin`
