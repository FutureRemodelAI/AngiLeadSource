#!/bin/sh

echo "Running database migrations..."

flask --app app:create_app db migrate || {
    echo "❌ Migration failed!"
    exit 1
}

echo "Starting Flask server..."
exec flask --app app:create_app run --host=0.0.0.0 --port=5000