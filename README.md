# E.L.Y.A.S.-A.I. Backend V1

Backend iniziale per la piattaforma Spirits Tech: SaaS cask monitoring, exchange, marketplace e dashboard data.

## Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Auth
- Docker Compose

## Avvio rapido

```bash
cp .env.example .env
docker compose up --build
```

API:
```txt
http://localhost:8000
```

Docs:
```txt
http://localhost:8000/docs
```

## Demo login

```txt
email: demo@investor.com
password: demo123
```

## Endpoint principali

```txt
POST /api/v1/auth/login
GET  /api/v1/users/me
GET  /api/v1/casks
GET  /api/v1/casks/{cask_id}
GET  /api/v1/portfolio/summary
GET  /api/v1/exchange/casks
GET  /api/v1/exchange/bottles
GET  /api/v1/marketplace/offers
```

## Struttura

```txt
app/
  api/v1/        routes
  core/          config + security
  db/            database session
  models/        SQLAlchemy models
  schemas/       Pydantic schemas
  services/      business logic
```

## Prossimo step
- Collegare frontend HTML/React
- Migrare a Next.js dashboard
- Aggiungere Stripe/checkout
- Aggiungere WebSocket per live monitoring
- Aggiungere Alembic migrations
