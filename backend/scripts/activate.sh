#!/bin/bash
set -e

# Change to backend directory (in case script is run from elsewhere)
cd "$(dirname "$0")/.."

echo "🔍 Checking PostgreSQL connection..."
if ! pg_isready -q; then
    echo "Starting PostgreSQL..."
    brew services start postgresql@14
    
    for i in {1..30}; do
        if pg_isready -q; then
            echo "PostgreSQL is ready"
            break
        fi
        echo "Waiting for PostgreSQL... ($i/30)"
        sleep 1
    done
fi

echo "Activating virtual environment..."
# source .venv/bin/activate

echo "Setting up database tables..."
python -c "from app.database import create_tables; create_tables()"

echo "Starting FastAPI server at http://localhost:8000"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 