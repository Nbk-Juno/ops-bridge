# OpsBridge

**Operational asset tracking with automatic, async audit logging.**

OpsBridge is a two-service microservices backend for managing operational assets — equipment, personnel, and resources — where every state change is automatically captured in a structured audit trail via RabbitMQ, without the API layer ever thinking about it.

```
┌──────────────┐    HTTP     ┌──────────────────────────┐
│    Client    │────────────►│   service_a  (FastAPI)   │
└──────────────┘             │                          │
                             │  /auth  /assets  /audit  │
                             └────────────┬─────────────┘
                                          │              │
                                    SQLAlchemy      RabbitMQ
                                          │         asset_events
                                          ▼              │
                                   ┌────────────┐        │
                                   │ PostgreSQL │        ▼
                                   │  (assets)  │  ┌─────────────────────┐
                                   └────────────┘  │  service_b          │
                                          ▲        │  (consumer worker)  │
                                          │        └────────┬────────────┘
                                    SQLAlchemy              │
                                          └────────────────-┘
                                           (writes AuditLog)
```

---

## Motivation

In any operational context — logistics, field ops, infrastructure management — knowing *what changed* is just as important as knowing *what the current state is*. A standard CRUD API tells you an asset is "inactive", but it can't tell you when that happened, what triggered it, or what came before.

Most solutions bolt logging onto the API layer: a decorator here, a middleware there. It works until it doesn't — missed callsites, tight coupling, and a logging failure that takes down your write path.

OpsBridge takes a different approach. `service_a` does one thing: manage assets. The moment an asset is created, updated, or deleted, it fires an event into RabbitMQ and moves on. `service_b` picks up that event asynchronously and writes the audit record independently. The two concerns never touch. The audit trail is automatic, decoupled, and survives failures on either side.

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Make](https://www.gnu.org/software/make/)

### Setup

**1. Clone the repo**
```bash
git clone https://github.com/nbk-juno/ops-bridge.git
cd ops-bridge
```

**2. Configure environment**
```bash
cp .env.example .env
```

Open `.env` and fill in your values. The defaults work out of the box for local development.

**3. Start the stack**
```bash
make build
```

This builds both service images and starts PostgreSQL, RabbitMQ, `service_a`, and `service_b`.

**4. Explore the API**

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

---

## 📖 Usage

### Make Commands

| Command | Description |
|---|---|
| `make up` | Start all services in the background |
| `make down` | Stop all services |
| `make build` | Rebuild images and start |
| `make restart` | Full teardown and rebuild |
| `make logs` | Tail logs for all services |
| `make logs-a` | Tail `service_a` logs only |
| `make logs-b` | Tail `service_b` logs only |
| `make test` | Run the full test suite |
| `make clean` | Stop services and **delete the database volume** |

### API Reference

#### Auth

**Register a user**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "juno", "email": "juno@ops.io", "password": "secret123"}'
```

**Login and capture your token**
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "juno", "password": "secret123"}' | jq -r '.access_token')
```

All subsequent requests require `Authorization: Bearer $TOKEN`.

---

#### Assets

**Create an asset**
```bash
curl -X POST http://localhost:8000/assets/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SR-71",
    "asset_type": "equipment",
    "status": "active",
    "location": "Beale AFB",
    "asset_metadata": {"clearance": "top-secret"}
  }'
```

**List all assets**
```bash
curl http://localhost:8000/assets/ \
  -H "Authorization: Bearer $TOKEN"
```

**Get a specific asset**
```bash
curl http://localhost:8000/assets/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Update an asset** *(partial updates supported)*
```bash
curl -X PATCH http://localhost:8000/assets/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "maintenance"}'
```

**Delete an asset**
```bash
curl -X DELETE http://localhost:8000/assets/1 \
  -H "Authorization: Bearer $TOKEN"
```

Asset types: `equipment` | `personnel` | `resource`
Asset statuses: `active` | `inactive` | `maintenance`

---

#### Audit Logs

Every create, update, and delete fires an event into RabbitMQ. `service_b` consumes it and writes an `AuditLog` record — independently of the API response. Events are typed as `asset.created`, `asset.updated`, or `asset.deleted` and include the full asset payload at the time of the event.

**Get all audit logs**
```bash
curl http://localhost:8000/audit/ \
  -H "Authorization: Bearer $TOKEN"
```

**Get logs for a specific asset**
```bash
curl http://localhost:8000/audit/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

### Running Tests

Tests run against a separate test database (`TEST_DATABASE_URL` in `.env`). The production database is never touched.

```bash
make test
```

The test suite covers auth, full asset CRUD, and audit log endpoints — including unauthorized access cases.

---

### RabbitMQ Management UI

While the stack is running, the RabbitMQ dashboard is available at [http://localhost:15672](http://localhost:15672) (default credentials: `guest` / `guest`). Use it to monitor queue depths and message rates.

---

## 🤝 Contributing

### Clone the repo

```bash
git clone https://github.com/nbk-juno/ops-bridge.git
cd ops-bridge
```

### Configure your environment

```bash
cp .env.example .env
```

Fill in your values. You'll need a local PostgreSQL instance for the test database (`TEST_DATABASE_URL`) and a local RabbitMQ for `TEST_RABBITMQ_URL`. The easiest way is to spin up the Docker stack first — RabbitMQ and Postgres will be available on their published ports.

```bash
make up
```

### Run the test suite

```bash
make test
```

Tests use an isolated test database and never touch the production volume.

### Submit a pull request

Fork the repository, make your changes on a feature branch, and open a pull request to `main`. Please make sure the full test suite passes before submitting.
