#!/bin/sh
set -e

echo "running database migrations"
cd /app/models/db_schemes/minirag/
alembic upgrade head
cd /app
