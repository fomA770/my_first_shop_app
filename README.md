# Shop API

FastAPI e-commerce API with authentication, roles, and CRUD operations.

## Features

- User authentication (JWT)
- Role-based access control (admin, manager, customer)
- Product CRUD operations
- PostgreSQL with async SQLAlchemy
- Pytest tests

## Installation

```bash
# Clone repository
git clone git@github.com:your-username/shop_app.git
cd shop_app

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
# alembic upgrade head

# Start the server
uvicorn app.main:app --reload
