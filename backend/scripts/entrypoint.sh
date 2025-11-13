#!/bin/sh
set -e

echo "Starting application..."

# Run migrations
python scripts/run_migrations.py

# Start the application
exec "$@"

