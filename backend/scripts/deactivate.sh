#!/bin/bash

echo "Stopping FastAPI server..."
pkill -f "uvicorn app.main:app" || echo "No uvicorn process found"

echo "Stopping PostgreSQL..."
brew services stop postgresql@14

echo "All services stopped"
