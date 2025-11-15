# Smart Campus Wallet - FastAPI Backend

A production-ready FastAPI backend for the Smart Campus Wallet application, designed to help students manage campus payments, budgets, and daily life.

## Features

- **Authentication & Authorization**: JWT-based authentication with secure password hashing
- **Spending Dashboard**: Track and analyze spending across categories
- **Budgeting & Goals**: Set budgets and track spending against limits
- **Campus Payments Hub**: Simulate payments for events, clubs, and services

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vegvisir_backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Set up the database:
```bash
# Using Docker Compose
docker-compose up -d postgres

# Or use your own PostgreSQL instance
# Update DATABASE_URL in .env
```

6. Run migrations:
```bash
alembic upgrade head
```

7. Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
vegvisir_backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── dependencies.py      # Shared dependencies
│   ├── exceptions.py        # Exception handlers
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic layer
│   └── api/                 # API routes
├── alembic/                 # Database migrations
├── tests/                   # Test suite
└── requirements.txt         # Python dependencies
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info

### Transactions
- `GET /api/v1/transactions/` - List transactions (with filters)
- `POST /api/v1/transactions/` - Create transaction
- `GET /api/v1/transactions/analytics` - Get spending analytics
- `GET /api/v1/transactions/{id}` - Get transaction details
- `PUT /api/v1/transactions/{id}` - Update transaction
- `DELETE /api/v1/transactions/{id}` - Delete transaction

### Budgets
- `GET /api/v1/budgets/` - List budgets
- `POST /api/v1/budgets/` - Create budget
- `GET /api/v1/budgets/{id}` - Get budget with tracking
- `PUT /api/v1/budgets/{id}` - Update budget
- `DELETE /api/v1/budgets/{id}` - Delete budget
- `GET /api/v1/budgets/tracking` - Get all budgets with status

### Payments
- `GET /api/v1/payments/` - List payments
- `POST /api/v1/payments/` - Create payment (simulate)
- `GET /api/v1/payments/{id}` - Get payment details
- `POST /api/v1/payments/{id}/complete` - Mark payment as completed

## Testing

Run tests with pytest:
```bash
pytest
```

## Development

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

## License

MIT

