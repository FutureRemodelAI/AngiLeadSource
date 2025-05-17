#!/bin/sh

# Load environment variables from .env file if present
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "Running database migrations..."

flask --app app:create_app db upgrade || {
    echo "❌ Migration failed!"
    exit 1
}

echo "Starting Flask server..."
exec flask --app app:create_app run --host=0.0.0.0 --port=${FLASK_RUN_PORT:-5000}
